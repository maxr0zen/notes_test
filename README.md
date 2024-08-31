# notes_test

Данное тестовое задание реализовано на FastAPI(с использованием REST API), с базой данных на Mongodb и с использоваением Dockerker.

Роуты для тестирования(можно использовать /docs, в FastAPI интегрирован swagger)
  Пользователи:
    /register - регистрация нового пользователя
    POST - http://localhost:8080/register
    Пример запроса:
     {
      "username": "testuser",
      "password": "testpassword"
    }
    Ответ
    {
      "message": "User registered successfully"
    }
    /login - авторизация пользователя
    POST - http://localhost:8080/login
    Пример запроса:
    {
      "username": "testuser",
      "password": "testpassword"
    }
    Ответ:
    {
      "access_token": "JWT токен пользователя",
      "token_type": "bearer"
    }

Заметки: - (В Headers должен быть хэдэр "Authorization": "Bearer JWT_токен_пользователя"
  /notes
  POST - http://127.0.0.1:8080/notes/ - Запись новой заметки
  Пример запроса:
  {
    "title": "Какой-та тайтл",
    "content": "Кокое-то садержание"
  }
  Ответ:
  {
    "title": "Какой-то тойтл",
    "content": "Какое-то содержание",
    "id": "66d295f9ff25836e97a7382a",
    "owner": "testuser"
  }
  GET - http://127.0.0.1:8080/notes/ - Вывод всех заметок пользователя
  Пример:
  [
    {
        "title": "Новая заметка с ошибками",
        "content": "Это контент имеет ошибки",
        "id": "66d28ff731cdb0c22b14e9c7",
        "owner": "testuser"
    },
    {
        "title": "Новая заметка с ошибками",
        "content": "Это контент имеет ошибки",
        "id": "66d2905731cdb0c22b14e9c8",
        "owner": "testuser"
    },
    {
        "title": "Какой-то тойтл",
        "content": "Какое-то содержание",
        "id": "66d295f9ff25836e97a7382a",
        "owner": "testuser"
    }
  ]
  GET - http://127.0.0.1:8080/notes/id_записи - просмотр конкретной записи по ее id
  Пример ответа:
  {
    "title": "Какой-то тойтл",
    "content": "Какое-то содержание",
    "id": "66d295f9ff25836e97a7382a",
    "owner": "testuser"
}
PUT - http://127.0.0.1:8080/notes/id_записи - редактирование записи по ее id
  Пример запроса:
  {
    "title": "Какой-та обнавленный тайтл",
    "content": "Кокое-то обнавленае садержание"
  }
  Пример ответа:
  {
    "title": "Какой-то обновленный тойтл",
    "content": "Какое-то обновление содержание",
    "id": "66d295f9ff25836e97a7382a",
    "owner": "testuser"
}
DELETE - http://127.0.0.1:8080/notes/id_записи - удаление записи по ее id
Ответ:
{
    "message": "Note deleted successfully"
}
  
