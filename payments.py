from fastapi import APIRouter
from bank_app.bank_app_db import BankAccount
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()
bank_account = BankAccount()


class Transfer(BaseModel):
    user_id_from: int
    user_id_to: int
    amount: Decimal


@router.post("/payments/founds_transfer/")
async def founds_transfer(transfer: Transfer):
    bank_account.founds_transfer(
        user_id_from=transfer.user_id_from,
        user_id_to=transfer.user_id_to,
        amount=transfer.amount,
    )


@router.post("/payments/{user_id}/card_payment/")
async def card_payment(user_id: int, amount: Decimal):
    payment_status = bank_account.card_payment(user_id, amount)
    if payment_status:
        return {
            "message": f"Payment of {amount} successfully processed for user {user_id}."
        }
    else:
        return {"error": f"Payment declined for user {user_id}."}


@router.post("/payments/{user_id}/reset_balance/")
async def reset_balance(user_id: int):
    bank_account.reset_balance(user_id=user_id)
    return {"message": f"User {user_id} balance successfully reset."}
