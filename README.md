# Privet.Api

<b>'api/v1/student/profile/<int:pk>/'</b> – Страница профиля студента, где <int:pk> его id. Для доступа передается токен.<br>
 Для выполнения доступны GET, PUT, PATCH, DELETE, HEAD, OPTIONS запросы. Данные передаются в виде:<br>
 ```
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
```
Citizenship – текстовое поле(должен быть список со странами, но пока так)<br>
Email – поле формата EmailField<br>
full_name – текстовое поле<br>
sex – поле со значением либо “male” либо “female”<br>
birth_date – поле даты в формате “YYYY-MM-DD”<br>
native_language – текствое поле<br>
other_languages_and_levels – текстовое поле<br>
vk – текстовое поле<br>
phone – цифровое поле<br>
telegram – текстовое поле<br>
whatsapp – текстовое поле<br>

<b>'api/v1/buddy/profile/<int:pk>/'</b> – Профиль сопровождающего, где <int:pk> его id.<br>
Для доступа передается токен.
Для выполнения доступны GET, PUT, PATCH, DELETE, HEAD, OPTIONS запросы.<br>
Структура запроса такая же, как и у студента, за исключением поля buddy_status:
```
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
```

buddy_status – текстовое поле(заглушка, поле должно присваиваться автоматически)<br>
</b>'api/v1/signup/student/'</b> – Регистрация студента. Выполняет POST запрос в виде:
```
{
    "university": "urfu",
    "email": "test@test.com",
    "password": "12345qwerty"
}
```
University – текстовое поле<br>
Email – поле EmailField<br>
Password – текстовое поле<br>
Выдаёт ответ в виде:<br>
```
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
```
<b>'api/v1/signup/buddy/'</b> – Регистрация сопровождающего. Всё аналогично студенту, за исключением того, чтобы выводит поле “is_buddy”: true

<b>'api/v1/login/'</b> – вход в аккаунт. POST запрос в виде:
```
{
     “email”: “test@test.com”,
     “password”:”12345qwerty”
}
```
Email – поле EmailField<br>
Password – текстовое поле<br>
Выдает ответ в виде:<br>
```
{
    "token": "a07de221d6a9834f92d3e2289b3929493557568f",
    "user_id": 27,
    "is_buddy": true
}
```
 Поле is_buddy принимает свое значение в зависимости от типа пользователя<br>
<b>'api/v1/logout/'</b> – Выход из аккаунта. Передается только токен в заголовке<br>

