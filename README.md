# Privet.Api

'api/v1/student/profile/<int:pk>/' – Страница профиля студента, где <int:pk> его id. Для доступа передается токен.
 Для выполнения доступны GET, PUT, PATCH, DELETE, HEAD, OPTIONS запросы. Данные передаются в виде:
{
    "citizenship": "test",
    "user":{
        "email": "testemail1@gmail.com",
        "user_info":{
            "full_name": "Иванов Иван",
            "sex": "male",
            "birth_date": "1990-01-01",
            "native_language": "русский",
            "other_languages_and_levels": "английский - B2",
            "contacts": {
                "vk": "https://vk.com/ivanov",
                "phone": "726789",
                "telegram": "@ivanov",
                "whatsapp": "+79123456789"
            }
        }
    }
}
Citizenship – текстовое поле(должен быть список со странами, но пока так)
Email – поле формата EmailField
full_name – текстовое поле
sex – поле со значением либо “male” либо “female”
birth_date – поле даты в формате “YYYY-MM-DD”
native_language – текствое поле
other_languages_and_levels – текстовое поле
vk – текстовое поле
phone – цифровое поле
telegram – текстовое поле
whatsapp – текстовое поле

'api/v1/buddy/profile/<int:pk>/' – Профиль сопровождающего, где <int:pk> его id. Для доступа передается токен.
Для выполнения доступны GET, PUT, PATCH, DELETE, HEAD, OPTIONS запросы. Структура запроса такая же, как и у студента, за исключением поля buddy_status:
{
    "buddy_status": "is_buddy",
    "user":{
        "email": "testemail1@gmail.com",
        "user_info":{
            "full_name": "Иванов Иван",
            "sex": "male",
            "birth_date": "1990-01-01",
            "native_language": "русский",
            "other_languages_and_levels": "английский - B2",
            "contacts": {
                "vk": "https://vk.com/ivanov",
                "phone": "726789",
                "telegram": "@ivanov",
                "whatsapp": "+79123456789"
            }
        }
    }
}

buddy_status – текстовое поле(заглушка, поле должно присваиваться автоматически)
'api/v1/signup/student/' – Регистрация студента. Выполняет POST запрос в виде:
{
    "university": "urfu",
    "email": "test@test.com",
    "password": "12345qwerty"
}
University – текстовое поле
Email – поле EmailField
Password – текстовое поле
Выдаёт ответ в виде:
{
    "user": {
        "university": "urfu",
        "email": "test@test.com",
        "password": "pbkdf2_sha256$600000$aA2cQT14uPoQXbuWHl6AlX$3fvcBTul2s+yjRUyytlTVirSa1rkqSXdwLLSGS2oQN4=",
        "is_buddy": false
    },
    "token": "a07de221d6a9834f92d3e2289b3929493557568f",
    "message": "account created"
}

'api/v1/signup/buddy/' – Регистрация сопровождающего. Всё аналогично студенту, за исключением того, чтобы выводит поле “is_buddy”: true

'api/v1/login/' – вход в аккаунт. POST запрос в виде:
{
     “email”: “test@test.com”,
     “password”:”12345qwerty”
}
Email – поле EmailField
Password – текстовое поле
Выдает ответ в виде:
{
    "token": "a07de221d6a9834f92d3e2289b3929493557568f",
    "user_id": 27,
    "is_buddy": true
}
 Поле is_buddy принимает свое значение в зависимости от типа пользователя
'api/v1/logout/' – Выход из аккаунта. Передается только токен в заголовке

