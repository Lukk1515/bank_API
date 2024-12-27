from fastapi import FastAPI
from bank_app.bank_app_db import BankAccount
from pydantic import BaseModel
from decimal import Decimal
from payments import router


bank_account = BankAccount()
app = FastAPI()
app.include_router(router, prefix="/payments", tags=["payments"])


class User(BaseModel):
    user_id: int
    balance: Decimal


@app.get("/users/")
async def list_users():
    users = bank_account.get_all_users()
    return {"users": users}


@app.post("/users/")
async def add_user(user: User):
    bank_account.add_user(user_id=user.user_id, balance=user.balance)
    return {"message": f"User {user.user_id} successfully added"}


@app.delete("/users/{user_id}")
async def delete_users(user_id: int):
    bank_account.remove_user(user_id=user_id)
    return {"message": f"User {user_id} successfully deleted"}


@app.get("/users/all/")
async def get_users_and_balance():
    users = bank_account.get_all_users()
    users_with_balance = [
        {
            "user_id": user_id,
            "balance": bank_account.get_balance(user_id),
        }
        for user_id in users
    ]
    return {"users": users_with_balance}


@app.post("/users/bulk_add/")
async def bulk_add_users(users: list[User]):
    users_data = [{"user_id": user.user_id, "balance": user.balance} for user in users]
    bank_account.add_multiple_users(users_data)
    return {"message": "All users added successfully"}
