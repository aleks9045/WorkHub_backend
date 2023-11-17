import sys

import aiofiles
from fastapi import UploadFile, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import EmailStr
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append("../../../GoodProject")

from backend.database import get_async_session
from backend.services.auth.utils import get_hashed_password, check_password, verify_password, \
    create_access_token, create_refresh_token, check_token
from backend.services.auth.models import UserModel
from backend.services.files.models import FileModel

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/register', summary="Create new user")
async def create_user(full_name: str, password: str, superuser: bool = False, yandex: str = None,
                      email: EmailStr = None,
                      specialization: str = None, status: str = None, photo: UploadFile = None,
                      session: AsyncSession = Depends(get_async_session)):
    if check_password(password):
        pass
    if yandex is not None and email is not None:
        result = await session.execute(select(UserModel.id).where(UserModel.email == email))
        if result.scalars().all():
            raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует.")
        result = await session.execute(select(UserModel.id).where(UserModel.yandex == yandex))
        if result.scalars().all():
            raise HTTPException(status_code=400, detail="Такой пользователь уже существует.")
    elif email is not None and yandex is None:
        result = await session.execute(select(UserModel.id).where(UserModel.email == email))
        if result.scalars().all():
            raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует.")
    elif email is None and yandex is not None:
        result = await session.execute(select(UserModel.id).where(UserModel.yandex == yandex))
        if result.scalars().all():
            raise HTTPException(status_code=400, detail="Такой пользователь уже существует.")
    else:
        raise HTTPException(status_code=400, detail="Введите почту.")

    try:
        if photo is not None:
            file_path = f'static/user_photo/{photo.filename}'
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = photo.file.read()
                await out_file.write(content)
            stmt = insert(FileModel).values(file_name=photo.filename, file_path=file_path)
            await session.execute(statement=stmt)
            await session.commit()
        elif photo is None:
            file_path = "static/user_photo/default.png"
        else:
            file_path = ""
        stmt = insert(UserModel).values(email=email,
                                        full_name=full_name,
                                        photo=file_path,
                                        yandex=yandex,
                                        superuser=superuser,
                                        specialization=specialization,
                                        status=status,
                                        hashed_password=get_hashed_password(password))
        await session.execute(statement=stmt)
        await session.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Произошла неизвестная ошибка.")
    return JSONResponse(status_code=201, content={"detail": "Пользователь был успешно добавлен"})


@router.post('/login', summary="Create access and refresh tokens")
async def login(password: str, yandex: str = None, email: EmailStr = None,
                session: AsyncSession = Depends(get_async_session)):
    if email is not None:
        result = await session.execute(select(UserModel.hashed_password).where(UserModel.email == email))
        result = result.scalars().all()

        if not result:
            raise HTTPException(status_code=400, detail="Неверно введена почта или пароль.")

        hashed_pass = result[0]
        result = await session.execute(select(UserModel.id).where(UserModel.email == email))
        user_id = result.scalars().all()[0]

    elif yandex is not None:
        result = await session.execute(select(UserModel.hashed_password).where(UserModel.yandex == yandex))
        result = result.scalars().all()

        if not result:
            raise HTTPException(status_code=400, detail="Неверно введен yandex или пароль.")

        hashed_pass = result[0]
        result = await session.execute(select(UserModel.id).where(UserModel.yandex == yandex))
        user_id = result.scalars().all()[0]
    else:
        raise HTTPException(status_code=400, detail="Введите почту.")
    if not verify_password(password, hashed_pass):
        raise HTTPException(status_code=400, detail="Неверно введена почта или пароль.")
    return JSONResponse(status_code=200, content={
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id)
    })


@router.get('/refresh', summary="Update access and refresh tokens")
async def get_new_tokens(request: Request,
                         session: AsyncSession = Depends(get_async_session)):
    payload = await check_token(request, False)
    query = select(UserModel.id).where(UserModel.id == int(payload["sub"]))
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return JSONResponse(status_code=200, content={
        "access_token": create_access_token(payload["sub"]),
        "refresh_token": create_refresh_token(payload["sub"])
    })


@router.get('/logout', summary="Logout")
async def logout(request: Request):
    await check_token(request, True)
    return Response(status_code=200)


@router.get('/me', summary="Get information about user")
async def get_user(request: Request, session: AsyncSession = Depends(get_async_session)):
    payload = await check_token(request, True)
    query = select(UserModel.email, UserModel.full_name, UserModel.photo).where(
        UserModel.id == int(payload["sub"]))
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return JSONResponse(status_code=200, content={"email": result[0][0],
                                                  "full_name": result[0][1],
                                                  "photo": result[0][2]})


# @router.delete('/me', summary="Delete user")
# async def delete_user(request: Request,
#                       session: AsyncSession = Depends(get_async_session)):
#     payload = await check_token(request, True)
#
#     query = select(UserModel.photo).where(UserModel.id == int(payload["sub"]))
#     result = await session.execute(query)
#     result = result.scalars().all()
#     os.remove(result[0])
#
#     stmt = delete(UserModel).where(UserModel.id == int(payload["sub"]))
#     await session.execute(stmt)
#     await session.commit()
#
#     return Response(status_code=200)


@router.patch('/me', summary="Change user's information")
async def patch_user(request: Request,
                     session: AsyncSession = Depends(get_async_session)):
    payload = await check_token(request, True)
    data = await request.json()
    stmt = update(UserModel).where(UserModel.id == int(payload["sub"])).values(full_name=data["full_name"])
    await session.execute(stmt)
    await session.commit()
    return Response(status_code=200)


# @router.patch('/photo', summary="Update user's photo")
# async def patch_photo(request: Request, photo: UploadFile,
#                       session: AsyncSession = Depends(get_async_session)):
#     payload = await check_token(request, True)
#     id_ = int(payload["sub"])
#     query = select(UserModel.photo).where(UserModel.id == id_)
#     result = await session.execute(query)
#     result = result.scalars().all()
#     if result[0] != photo.filename and result[0] != "static/user_photo/default.png":
#         os.remove(result[0])
#     try:
#         file_path = f'static/user_photo/{photo.filename}'
#         async with aiofiles.open(file_path, 'wb') as out_file:
#             content = photo.file.read()
#             await out_file.write(content)
#         stmt = update(FileModel).where(FileModel.file_path == result[0]).values(file_name=photo.filename,
#                                                                                 file_path=file_path)
#         await session.execute(statement=stmt)
#         await session.commit()
#         stmt = update(UserModel).where(UserModel.id == id_).values(photo=file_path)
#         await session.execute(statement=stmt)
#         await session.commit()
#     except Exception:
#         raise HTTPException(status_code=400, detail="Произошла неизвестная ошибка.")
#
#     return Response(status_code=200)
#
#
# @router.delete('/photo', summary="Delete user's photo")
# async def delete_photo(request: Request,
#                        session: AsyncSession = Depends(get_async_session)):
#     payload = await check_token(request, True)
#     try:
#         id_ = int(payload["sub"])
#         query = select(UserModel.photo).where(UserModel.id == id_)
#         result = await session.execute(query)
#         result = result.scalars().all()
#         os.remove(result[0])
#         stmt = update(UserModel).where(UserModel.id == id_).values(photo="static/user_photo/default.png")
#         await session.execute(statement=stmt)
#         await session.commit()
#     except Exception:
#         raise HTTPException(status_code=400, detail="Произошла неизвестная ошибка.")
#
#     return Response(status_code=200)


@router.get('/all', summary="List of all users")
async def patch_user(session: AsyncSession = Depends(get_async_session)):
    query = select(UserModel.id, UserModel.superuser, UserModel.full_name, UserModel.specialization, UserModel.status,
                   UserModel.photo).where(1 == 1).order_by(UserModel.id)
    result = await session.execute(query)
    result = result.all()
    res_dict = []
    for i in result:
        if not i[1]:
            res_dict.append({"id": i[0],
                             "full_name": i[2],
                             "specialization": i[3],
                             "status": i[4],
                             "photo": i[5]})
    return JSONResponse(status_code=200, content=res_dict)


@router.patch('/proffessional', summary="Change user's information")
async def patch_user(id_: int, specialization: str = None, status: str = None,
                     session: AsyncSession = Depends(get_async_session)):
    stmt = update(UserModel).where(UserModel.id == id_).values(specialization=specialization,
                                                               status=status)
    await session.execute(stmt)
    await session.commit()
    return Response(status_code=200)
