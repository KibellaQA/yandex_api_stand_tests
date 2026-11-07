
import configuration
import requests
import data


# Отправка POST-запроса на создание пользователя
def post_new_user(body):
    return requests.post(
        configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
        json=body,
        headers=data.headers
    )


# Получение таблицы пользователей
def get_users_table():
    return requests.get(
        configuration.URL_SERVICE + configuration.USERS_TABLE_PATH
    )
