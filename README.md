# Privet.Api
Это API для https://github.com/K0ch3rga/Privet

<b>'api/v1/student/profile/<int:pk>/'</b> – Страница профиля студента, где <int:pk> его id. Для доступа передается токен.<br>
 Для выполнения доступны GET, PUT, PATCH, DELETE, HEAD, OPTIONS запросы. Данные передаются в виде:<br>
 ```
{
    "citizenship": "Kazakhstan",
    "sex": "male",
    "user": {
        "email": "test50@test.com",
        "university": "test",
        "user_info": {
            "full_name": "abcde abcde",
            "birth_date": "1990-01-28",
            "native_language": "русский",
            "other_languages_and_levels": [
                {
                    "other_language_and_level": "test"
                }
            ],
            "contacts": {
                "vk": "https://vk.com/ivanov",
                "phone": "726789",
                "telegram": "@ivanov",
                "whatsapp": "+79123456789"
            }
        }
    },
    "profile_type": "student",
    "last_buddy": "",
    "last_arrival_date": "",
    "institute": "rtf",
    "study_program": "test1",
    "last_visa_expiration": "1991-08-01",
    "accommodation": "Ekaterinburg"
}
```
Citizenship – текстовое поле(должен быть список со странами, но пока так)<br>
sex – поле со значением либо “male” либо “female”<br>
Email – поле формата EmailField<br>
university - текстовое поле<br>
full_name – текстовое поле<br>
birth_date – поле даты в формате “YYYY-MM-DD”<br>
native_language – текствое поле<br>
other_language_and_level – текстовое поле<br>
vk – текстовое поле<br>
phone – цифровое поле<br>
telegram – текстовое поле<br>
whatsapp – текстовое поле<br>
profile_type - заполняется автоматически<br>
last_buddy - заполняется автоматически<br>
last_arrival_date - заполняется автоматически<br>
institute - текстовое поле, заполняется студентом<br>
study_program - текстовое поле, заполняется студентом<br>
last_visa_expiration - поле даты в формате “YYYY-MM-DD”, заполняется студентом<br>
accommodation -текстовое поле, заполняется студентом<br>

<b>'api/v1/buddy/profile/<int:pk>/'</b> – Профиль сопровождающего, где <int:pk> его id.<br>
Для доступа передается токен.
Для выполнения доступны GET, PUT, PATCH, DELETE, HEAD, OPTIONS запросы.<br>
Структура запроса такая же, как и у студента, за исключением поля buddy_status и city, а также отсутствуют поля sex и citizenship:
```
{
    "city": "test1",
    "user": {
        "email": "test49@test.com",
        "university": "test",
        "user_info": {
            "full_name": "test49",
            "birth_date": "1991-08-01",
            "native_language": "test",
            "other_languages_and_levels": [
                {
                    "other_language_and_level": "test"
                }
            ],
            "contacts": {
                "vk": "test1",
                "phone": "111111111111",
                "telegram": "test",
                "whatsapp": "test"
            }
        }
    },
    "profile_type": "buddy",
    "buddy_status": false
}
```
city - текстовое поле<br>
buddy_status – логическое поле, изменять может тимлид, false - неподтвержденный статус, true - подтвержденный<br>
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
После выполнения POST запроса отправляет код для подтверждения регистрации на указанную почту
<b>'api/v1/confirm/student/'</b> - Подтверждение регистрации студента. POST запрос в виде:
```
{
    "code": "123456",
    "user_id": "12"
}
```
code - код, высланный на почту<br>
user_id - id пользователя, которого регистрируем<br>
Выдает ответ в виде:
```
{
    "message": "Регистрация успешна.",
    "token": "e067c3a1f34be27f3131ace783e07a3bc8aa1a5f"
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
<br>
<b>'api/v1/student/arrival-booking/<int:pk>/'</b> - Регистрация приезда студентом. PUT/PATCH запрос в виде (При GET запросе возвращает те же данные):
```
{
    "citizenship": "Kazakhstan",
    "sex": "male",
    "user": {
        "user_info": {
            "full_name": "abcde abcde",
            "contacts": {
                "vk": "https://vk.com/ivanov",
                "phone": "726789",
                "telegram": "@ivanov",
                "whatsapp": "+79123456789"
            }
        }
    },
    "arrival_booking": {
        "id": 4,
        "tickets": [
            {
                file: "file"
            }
        ],
        "arrival_date": "2023-12-29",
        "arrival_time": "15:00:00",
        "flight_number": "10101",
        "arrival_point": "Ekaterinburg",
        "comment": "",
        "other_students": [
            53
        ]
    }
}
```
"citizenship", "sex" и "user" имеют тот же вид, что и в странице профиля студента<br>
arrival_booking:<br>
arrival_date - дата прибытия в формате "YYYY-MM-DD"<br>
arrival_time - время прибытия в формате "HH:MM"<br>
flight_number - текстовое поле<br>
arrival_point - текстовое поле<br>
comment - текстовое поле<br>
other_students - id дополнительных участников приезда<br>
<b>'api/v1/send-email/'</b> - Отправляет код для подтверждения смены пароля на указанный email. POST запрос в виде:
```
{
    "email": "jodix98630@pursip.com"
}
```
<b>'api/v1/confirm-email/'</b> - Подтверждение кода для смены пароля. POST запрос в виде:
```
{
    "code": "910926"
}
```
<b>'api/v1/update-password/'</b> - Смена пароля. POST запрос в виде:
```
{
    "password": "12345qwerty",
    "user_id": "61"
}
```
<b>'api/v1/student/arrival-booking/add-student/'</b> - Добавление дополнительных участников приезда. POST запрос в виде:
```
{
    "student_name": "abcde abcde",
    "student_id": "47"
}
```
student_name - имя студента, добавляемого в приезд<br>
student_id - id студента, к которому добавляем<br>
<b>'api/v1/buddy/arrivals/'</b> - Вывод всех приездов. GET запрос, ответ в виде:
```
[
    {
        "id": 1,
        "arrival_date": "2023-01-01",
        "buddies_amount": 1,
        "group_full_names": "test abc",
        "group_countries": "test test"
    },
]
```
id - id приезда<br>
arrival_data - дата приезда<br>
buddyies_amount - количество сопровождающих на приезде<br>
group_full_names - имена всех студентов в приезде<br>
group_countries - страны всех студентов в приезда<br>
<b>'api/v1/buddy/arrivals/<int:pk>/'</b> - просмотр конкретного приезда по его id = <int:pk>. GET запрос возвращает:
```
{
    "id": 3,
    "other_students": [
        {
            "citizenship": "Kazakhstan",
            "user": {
                "user_info": {
                    "full_name": "abcde abcde",
                    "sex": "male",
                    "contacts": {
                        "vk": "https://vk.com/ivanov",
                        "phone": "726789",
                        "telegram": "@ivanov",
                        "whatsapp": "+79123456789"
                    }
                }
            }
        }
    ],
    "arrival_date": "2023-12-16",
    "arrival_time": "15:00:00",
    "flight_number": "1",
    "arrival_point": "1",
    "comment": "",
    "full_name": "testtt1",
    "sex": "male",
    "citizenship": "Kazakhstan",
    "vk": "https://vk.com/ivanov",
    "phone": "726789",
    "telegram": "@ivanov",
    "whatsapp": "+79123456789",
    "buddy_full_names": [
        "test49"
    ]
}
```
buddy_full_names - имена сопровождающих, записанных на приезд<br>
other_students относится к студенту, добавленному как дополнительный участник<br>
остальный поля относятся к студенту, создающему приезд<br>
<b>'api/v1/buddy/add-arrival/'</b> - Добавление сопровождающего на приезд. POST запрос в виде:
```
{
    "buddy_id": "49",
    "student_id": "47"
}
```
buddy_id - id сопровождающего<br>
student_id - id студента, который создал приезд<br>
<b>'api/v1/buddy/buddy-arrivals/<int:user>/'</b> - Вывод всех приездов, на которые записан сопровождающий с id <int:pk>. GET запрос возвращает:
```
{
    "user": 49,
    "buddy_arrivals": [
        {
            "student": {
                "citizenship": "Kazakhstan",
                "user": {
                    "email": "test47@test.com",
                    "user_info": {
                        "full_name": "testtt1",
                        "sex": "male",
                        "birth_date": "1990-01-28",
                        "native_language": "русский",
                        "other_languages_and_levels": "",
                        "contacts": {
                            "vk": "https://vk.com/ivanov",
                            "phone": "726789",
                            "telegram": "@ivanov",
                            "whatsapp": "+79123456789"
                        }
                    }
                },
                "arrival_booking": {
                    "id": 3,
                    "other_students": [
                        {
                            "user": {
                                "email": "test48@test.com",
                                "user_info": {
                                    "full_name": "abcde abcde",
                                    "sex": "male",
                                    "birth_date": "1990-01-28",
                                    "native_language": "русский",
                                    "other_languages_and_levels": "",
                                    "contacts": {
                                        "vk": "https://vk.com/ivanov",
                                        "phone": "726789",
                                        "telegram": "@ivanov",
                                        "whatsapp": "+79123456789"
                                    }
                                }
                            },
                            "citizenship": "Kazakhstan",
                        }
                    ],
                    "arrival_date": "2023-12-16",
                    "arrival_time": "15:00:00",
                    "flight_number": "1",
                    "arrival_point": "1",
                    "comment": ""
                }
            }
        }
    ],
    "buddy_status": "buddy"
}
```
<b>'api/v1/buddy/student/<int:pk>/'</b> - Редактирование сопровождающим полей в профиле студента с id <int:pk>. PUT/PATCH запрос в виде:
```
{
    "only_view": {
        "institute": "rtf",
        "study_program": "test1",
        "last_visa_expiration": "2023-12-21",
        "accommodation": "Ekaterinburg",
        "buddys_comment": "test"
    }
}
```
institute - текстовое поле<br>
study_program - текстовое поле<br>
last_visa_expiration - дата, в формате "YYYY-MM-DD"<br>
accommodation - текстовое поле<br>
buddys_comment - текстовое поле<br>
GET запрос выдает ответ в виде:
```
{
    "only_view": {
        "institute": "rtf",
        "study_program": "test1",
        "last_visa_expiration": "1991-08-01",
        "accommodation": "Ekaterinburg",
        "buddys_comment": "test"
    },
    "citizenship": "Kazakhstan",
    "sex": "male",
    "user": {
        "email": "test50@test.com",
        "user_info": {
            "full_name": "abcde abcde",
            "birth_date": "1990-01-28",
            "native_language": "русский",
            "other_languages_and_levels": [
                "test"
            ],
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
<b>'api/v1/buddy/buddy-students/<int:pk>/'</b> - Список всех студентов сопровождающего. GET запрос возвращает:
```

    {
        "arrival_id": 3,
        "student_full_name": "testtt1",
        "citizenship": "Kazakhstan",
        "student_id": 47
    },
    {
        "arrival_id": 3,
        "student_full_name": "abcde abcde",
        "citizenship": "Kazakhstan",
        "student_id": 48
    }
]
```
<b>'api/v1/teamlead/add-buddy-to-arrival/'</b> - Добавление тимлидом сопровождающего на приезд. POST запрос в виде:
```
{
    "arrival_booking_id": "3",
    "buddy_id": "55"
}
```
arrival_booking_id - id приезда<br>
buddy_id - id сопровождающего<br>
<b>'api/v1/teamlead/delete-arrival/'</b> - Удаление тимлидом сопровождающего из приезда. DELETE запрос в виде:
```
{
    "buddy_id": "55",
    "buddy_arrival_id": "3"
}
```
buddy_id - id сопровождающего<br>
buddy_arrival_id - id приезда<br>

