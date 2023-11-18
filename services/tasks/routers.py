import sys

import requests
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append("../../../GoodProject")

from backend.database import get_async_session
from backend.services.tasks.models import TaskModel, StatusModel
from backend.services.auth.models import UserModel

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@router.post('/add', summary="Create new task")
async def create_task(description: str, contact: str,
                      session: AsyncSession = Depends(get_async_session)):
    response = requests.post(f'http://ml:4000/api/ml_model?utterance={description}')
    response_json = response.json()

    query = select(UserModel.superuser, UserModel.email, UserModel.busy).where(1 == 1).order_by(UserModel.id)
    result = await session.execute(query)
    result = result.all()
    professionals = dict()
    for i in result:
        query = select(StatusModel.is_competent_in_payment_issue,
                       StatusModel.is_competent_in_create_account,
                       StatusModel.is_competent_in_contact_customer_service,
                       StatusModel.is_competent_in_get_invoice,
                       StatusModel.is_competent_in_track_order,
                       StatusModel.is_competent_in_get_refund,
                       StatusModel.is_competent_in_contact_human_agent,
                       StatusModel.is_competent_in_recover_password,
                       StatusModel.is_competent_in_change_order,
                       StatusModel.is_competent_in_delete_account,
                       StatusModel.is_competent_in_complaint,
                       StatusModel.is_competent_in_check_invoices,
                       StatusModel.is_competent_in_review,
                       StatusModel.is_competent_in_check_refund_policy,
                       StatusModel.is_competent_in_delivery_options,
                       StatusModel.is_competent_in_check_cancellation_fee,
                       StatusModel.is_competent_in_track_refund,
                       StatusModel.is_competent_in_check_payment_methods,
                       StatusModel.is_competent_in_switch_account,
                       StatusModel.is_competent_in_newsletter_subscription,
                       StatusModel.is_competent_in_delivery_period,
                       StatusModel.is_competent_in_edit_account,
                       StatusModel.is_competent_in_registration_problems,
                       StatusModel.is_competent_in_change_shipping_address,
                       StatusModel.is_competent_in_set_up_shipping_address,
                       StatusModel.is_competent_in_place_order,
                       StatusModel.is_competent_in_cancel_order,
                       StatusModel.is_competent_in_check_invoice).where(StatusModel.email == i[1])
        result = await session.execute(query)
        keys = result.keys()
        for k in keys:
            if k.endswith(response_json['category']):
                professionals[i[2]] = i[1]
    if professionals != {}:
        best = professionals[min(professionals.keys())]
        best_min = min(professionals.keys())
    else:
        raise HTTPException(status_code=400, detail="Нет ответчиков.")

    stmt = insert(TaskModel).values(email=best,
                                    description=description,
                                    category=response_json['category'],
                                    importance=response_json['importance'],
                                    contact=contact)
    await session.execute(statement=stmt)
    await session.commit()

    stmt = update(UserModel).where(UserModel.email == best).values(busy=best_min + 1)
    await session.execute(statement=stmt)
    await session.commit()

    return JSONResponse(status_code=201, content={"email": best,
                                                  "description": description,
                                                  "category": response_json['category'],
                                                  "importance": response_json['importance'],
                                                  "contact": contact})


@router.get('/get', summary="Get task")
async def create_task(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(TaskModel.description, TaskModel.contact, TaskModel.category, TaskModel.importance,
                   TaskModel.id).where(
        TaskModel.email == email)
    result = await session.execute(query)
    result = result.all()
    res_dict = []
    for i in result:
        res_dict.append({"id": i[4],
                         "description": i[0],
                         "contact": i[1],
                         "category": i[2],
                         "importance": i[3]})
    return JSONResponse(status_code=200, content=res_dict)


@router.delete('/delete', summary="Delete task")
async def create_task(id_: int, session: AsyncSession = Depends(get_async_session)):
    query = select(TaskModel.email).where(TaskModel.id == id_)
    result = await session.execute(query)
    result_email = result.all()

    query = select(UserModel.busy).where(UserModel.email == result_email[0][0])
    result = await session.execute(query)
    result_busy = result.all()

    stmt = update(UserModel).where(UserModel.email == result_email[0][0]).values(busy=result_busy[0][0] - 1)
    await session.execute(statement=stmt)
    await session.commit()

    query = delete(TaskModel).where(TaskModel.id == id_)
    result = await session.execute(query)
    return JSONResponse(status_code=200, content="Успешно")


@router.get('/all', summary="Get all tasks")
async def all_task(session: AsyncSession = Depends(get_async_session)):
    query = select(TaskModel.description, TaskModel.contact, TaskModel.category, TaskModel.importance,
                   TaskModel.id, TaskModel.email).where(1 == 1).order_by(TaskModel.id)
    result = await session.execute(query)
    result = result.all()
    res_dict = []
    for i in result:
        query = select(UserModel.email, UserModel.full_name, UserModel.photo).where(UserModel.email == i[5])
        result = await session.execute(query)
        result_user = result.all()
        for u in result_user:
            res_dict.append({"id": i[4],
                             "description": i[0],
                             "contact": i[1],
                             "category": i[2],
                             "importance": i[3],
                             "email": u[0],
                             "full_name": u[1],
                             "photo": u[2]
                             })
    return JSONResponse(status_code=200, content=res_dict)
