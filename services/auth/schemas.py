from pydantic import BaseModel


class StatusSchema(BaseModel):
    is_competent_in_payment_issue: bool
    is_competent_in_create_account: bool
    is_competent_in_contact_customer_service: bool
    is_competent_in_get_invoice: bool
    is_competent_in_track_order: bool
    is_competent_in_get_refund: bool
    is_competent_in_contact_human_agent: bool
    is_competent_in_recover_password: bool
    is_competent_in_change_order: bool
    is_competent_in_delete_account: bool
    is_competent_in_complaint: bool
    is_competent_in_check_invoices: bool
    is_competent_in_review: bool
    is_competent_in_check_refund_policy: bool
    is_competent_in_delivery_options: bool
    is_competent_in_check_cancellation_fee: bool
    is_competent_in_track_refund: bool
    is_competent_in_check_payment_methods: bool
    is_competent_in_switch_account: bool
    is_competent_in_newsletter_subscription: bool
    is_competent_in_delivery_period: bool
    is_competent_in_edit_account: bool
    is_competent_in_registration_problems: bool
    is_competent_in_change_shipping_address: bool
    is_competent_in_set_up_shipping_address: bool
    is_competent_in_place_order: bool
    is_competent_in_cancel_order: bool
    is_competent_in_check_invoice: bool
