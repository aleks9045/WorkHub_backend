# WorkHub_backend

## .env (must be in root directory)

```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
HOST=
PORT=""
SECRET_MANAGER=""
SECRET_JWT_REFRESH=""
SECRET_JWT=""
```

## Launch for local development

```
python -m venv venv
```

```
.\venv\Scripts\activate
```

```
pip install -r .\requirements.txt
```

```
alembic revision --autogenerate
```

```
alembic upgrade head
```

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Launch in docker

```
docker-compose up --build
```

## Used technologies

#### [FastApi](https://fastapi.tiangolo.com/)

#### [Sqlalchemy](https://www.sqlalchemy.org/)

#### [Alembic](https://alembic.sqlalchemy.org/en/latest/)

#### [Pydantic](https://docs.pydantic.dev/latest/)

#### [PostgreSQL](https://www.postgresql.org/)

# API Documentation(JWT Registration)

##

## auth/register [POST]

### Headers:

```
Content_Type: multipart/form-data
```

### Fields:

```
email - string(required)
name - string(required)
full_name - string(required)
password - string(required)
photo - string($binary)
```

### Responses:

```
400: {"detail": "Пользователь с такой почтой уже существует."}
400: {"detail": "Произошла неизвестная ошибка."
201: {"detail": "Пользователь был успешно добавлен."}
```

##

## auth/login [POST]

### Headers:

```
 Content_Type: multipart/form-data
```

### Fields:

```
 email - string(required)
 password - string(required)
```

### Responses:

```
 400: {"detail": "Неверно введена почта или пароль."}
 400: {"detail": "Пароль должен содержать минимум 8 символов."}
 400: {"detail": "Пароль должен содержать минимум 2 буквы разных регистров."}
 400: {"detail": "Пароль должен содержать минимум 1 специальный символ."}
 400: {"detail": "Пароль должен содержать минимум 1 цифру."}
 200: {"access_token": access_token,
       "refresh_token": refresh_token}
```

##

## auth/refresh [POST]

### Headers:

```
 Content_Type: multipart/form-data
 Authorization: "Bearer" "refresh_token"
```

### Fields:

```
 None
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 404: {"detail": "Пользователь не найден."}
 200: {"access_token": access_token,
       "refresh_token": refresh_token}
```

##

## auth/me [GET]

### Headers:

```
Content_Type: None
Authorization: "Bearer" "access_token"
```

### Fields:

```
 None
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 404: {"detail": "Пользователь не найден."}
 200: {"name": name,
       "full_name": full_name,
       "email": email,
       "photo": path_to_photo}
```

##

## auth/me [PATCH]

### Headers:

```
Content_Type: application/json
Authorization: "Bearer" "access_token"
```

### Fields:

```
 name - string(required)
 full_name - string(required)
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 200: None
```

##

## auth/me [DELETE]

### Headers:

```
Content_Type: None
Authorization: "Bearer" "access_token"
```

### Fields:

```
 None
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 200: None
```

##

## auth/logout [GET]

### Headers:

```
Content_Type: None
Authorization: "Bearer" "access_token"
```

### Fields:

```
 None
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 200: None
```

##

## auth/photo [PATCH]

### Headers:

```
Content_Type: multipart/form-data
Authorization: "Bearer" "access_token"
```

### Fields:

```
 photo - string($binary)
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 400: {"detail": "Произошла неизвестная ошибка."}
 200: None
```

##

## auth/photo [DELETE]

### Headers:

```
Content_Type: None
Authorization: "Bearer" "access_token"
```

### Fields:

```
 None
```

### Responses:

```
 400: {"detail": "Отсутствует заголовок с токеном."}
 401: {"detail": "Срок действия токена истёк."}
 403: {"detail": "Не удалось подтвердить учетные данные."}
 400: {"detail": "Произошла неизвестная ошибка."}
 200: None
```
