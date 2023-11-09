from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext

from backend.config import SECRET_JWT, SECRET_JWT_REFRESH

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 * 2  # 14 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = SECRET_JWT
JWT_REFRESH_SECRET_KEY = SECRET_JWT_REFRESH

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def check_password(password: str) -> bool:
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 8 символов.")
    if password.isdigit():
        raise HTTPException(status_code=400,
                            detail="Пароль должен содержать минимум 2 буквы разных регистров.")
    if password.islower():
        raise HTTPException(status_code=400,
                            detail="Пароль должен содержать минимум 2 буквы разных регистров.")
    if password.isupper():
        raise HTTPException(status_code=400,
                            detail="Пароль должен содержать минимум 2 буквы разных регистров.")
    if password.isalnum():
        raise HTTPException(status_code=400,
                            detail="Пароль должен содержать минимум 1 специальный символ.")
    if password.isalpha():
        raise HTTPException(status_code=400,
                            detail="Пароль должен содержать минимум минимум 1 цифру.")
    return True


def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def check_token(request, type_: bool) -> dict:
    try:
        try:
            authorization = request.headers.get("Authorization").split(" ")
        except AttributeError:
            raise HTTPException(
                status_code=400,
                detail="Отсутствует заголовок с токеном."
            )
        if authorization[0] != "Selezenka":
            raise HTTPException(status_code=400, detail="Не угадал.")
        if type_:
            payload = jwt.decode(authorization[1], JWT_SECRET_KEY, algorithms=[ALGORITHM])
        else:
            payload = jwt.decode(authorization[1], JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail="Срок действия токена истёк."
            )
    except jwt.JWTError:
        raise HTTPException(
            status_code=403,
            detail="Не удалось подтвердить учетные данные."
        )
    return payload
