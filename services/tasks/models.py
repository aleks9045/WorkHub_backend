from sqlalchemy import Column, Integer, String, Boolean

from backend.database import Base


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1024), nullable=False)
    contact = Column(String, nullable=False)


class StatusModel(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_competent_in_payment_issue = Column(Boolean, nullable=False)
    is_competent_in_create_account = Column(Boolean, nullable=False)
    is_competent_in_contact_customer_service = Column(Boolean, nullable=False)
    is_competent_in_get_invoice = Column(Boolean, nullable=False)
    is_competent_in_track_order = Column(Boolean, nullable=False)
    is_competent_in_get_refund = Column(Boolean, nullable=False)
    is_competent_in_contact_human_agent = Column(Boolean, nullable=False)
    is_competent_in_recover_password = Column(Boolean, nullable=False)
    is_competent_in_change_order = Column(Boolean, nullable=False)
    is_competent_in_delete_account = Column(Boolean, nullable=False)
    is_competent_in_complaint = Column(Boolean, nullable=False)
    is_competent_in_check_invoices = Column(Boolean, nullable=False)
    is_competent_in_review = Column(Boolean, nullable=False)
    is_competent_in_check_refund_policy = Column(Boolean, nullable=False)
    is_competent_in_delivery_options = Column(Boolean, nullable=False)
    is_competent_in_check_cancellation_fee = Column(Boolean, nullable=False)
    is_competent_in_track_refund = Column(Boolean, nullable=False)
    is_competent_in_check_payment_methods = Column(Boolean, nullable=False)
    is_competent_in_switch_account = Column(Boolean, nullable=False)
    is_competent_in_newsletter_subscription = Column(Boolean, nullable=False)
    is_competent_in_delivery_period = Column(Boolean, nullable=False)
    is_competent_in_edit_account = Column(Boolean, nullable=False)
    is_competent_in_registration_problems = Column(Boolean, nullable=False)
    is_competent_in_change_shipping_address = Column(Boolean, nullable=False)
    is_competent_in_set_up_shipping_address = Column(Boolean, nullable=False)
    is_competent_in_place_order = Column(Boolean, nullable=False)
    is_competent_in_cancel_order = Column(Boolean, nullable=False)
    is_competent_in_check_invoice = Column(Boolean, nullable=False)
