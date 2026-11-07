
import sender_stand_request
import data


# Создаем копию тела запроса и меняем имя
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Общая функция для позитивных проверок
def positive_assert(first_name):
    # Подготавливаем тело запроса
    user_body = get_user_body(first_name)

    # Отправляем POST-запрос на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяем код ответа
    assert user_response.status_code == 201

    # Проверяем, что токен не пустой
    assert user_response.json()["authToken"] != ""

    # Получаем таблицу пользователей
    users_table_response = sender_stand_request.get_users_table()

    # Формируем строку с данными созданного пользователя
    str_user = (
        user_body["firstName"] + ","
        + user_body["phone"] + ","
        + user_body["address"] + ",,,"
        + user_response.json()["authToken"]
    )

    # Проверяем, что пользователь записан в таблицу один раз
    assert users_table_response.text.count(str_user) == 1


# Тест 1. Имя из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Аа")


# Тест 2. Имя из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("А" + "а" * 14)


# Общая функция для негативных проверок имени
def negative_assert_symbol(first_name):
    # Подготавливаем тело запроса с нужным именем
    user_body = get_user_body(first_name)

    # Отправляем запрос на создание пользователя
    response = sender_stand_request.post_new_user(user_body)

    # Проверяем HTTP-статус
    assert response.status_code == 400

    # Проверяем код ошибки в теле ответа
    assert response.json()["code"] == 400

    # Проверяем текст ошибки
    assert response.json()["message"] == (
        "Имя пользователя введено некорректно. "
        "Имя может содержать только русские или латинские буквы, "
        "длина должна быть не менее 2 и не более 15 символов"
    )


# Тест 3. Имя пользователя состоит из одной буквы
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")


# Тест 4. Имя пользователя состоит из 16 букв
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("А" * 16)



# Тест 5. Имя пользователя из английских букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Имя пользователя из русских букв
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


# Тест 7. Имя пользователя содержит пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и КО")


# Тест 8. Имя пользователя содержит специальные символы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")


# Тест 9. Имя пользователя содержит цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


# Общая функция для тестов 10 и 11
def negative_assert_no_first_name(user_body):
    # Отправляем запрос
    response = sender_stand_request.post_new_user(user_body)

    # Проверяем HTTP-код ответа
    assert response.status_code == 400

    # Проверяем код ошибки в теле ответа
    assert response.json()["code"] == 400

    # Проверяем сообщение об ошибке
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 10. Ошибка 
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

    # Тест 11. Ошибка 
# Параметр firstName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

    
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
