import sys

import requests
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import insert, select
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


    query = select(UserModel.superuser, UserModel.email, UserModel.specialization).where(1 == 1).order_by(UserModel.id)
    result = await session.execute(query)
    result = result.all()
    res_dict = []
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
        status_result = result.all()
        keys = result.keys()
        for k in keys:
            if k.endswith(response_json['category']):
                stmt = insert(TaskModel).values(email=i[1],
                                                description=description,
                                                category=response_json['category'],
                                                importance=response_json['importance'],
                                                contact=contact)
                await session.execute(statement=stmt)
                await session.commit()

                return JSONResponse(status_code=201, content={"email": i[1],
                                                "description": description,
                                                "category": response_json['category'],
                                                "importance": response_json['importance'],
                                                "contact": contact})
