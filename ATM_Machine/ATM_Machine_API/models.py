from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    account_number: str
    pin: str
    balance: float
    full_name: str
    address: str
    blood_group: str

class User(UserCreate):
    pass

class Transaction(BaseModel):
    id: int
    account_number: str
    transaction_type: str
    amount: float
    timestamp: str
