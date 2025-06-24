import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
from src.database import Base
from pydantic import BaseModel

# SQLAlchemy Models
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    pin = Column(String)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    type = Column(String)  # "deposit" or "withdraw"
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    account = relationship("Account", back_populates="transactions")

# Pydantic Models
class AccountBase(BaseModel):
    account_number: str
    pin: str

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    pin: Optional[str] = None
    balance: Optional[float] = None

class AccountSchema(AccountBase):
    id: int
    balance: float
    created_at: datetime
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    type: str
    amount: float

class TransactionCreate(TransactionBase):
    account_number: str

class TransactionSchema(TransactionBase):
    id: int
    account_id: int
    timestamp: datetime
    class Config:
        orm_mode = True