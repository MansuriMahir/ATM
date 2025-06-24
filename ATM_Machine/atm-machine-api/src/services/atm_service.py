import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import HTTPException
from src.models.account import Account, AccountCreate, AccountUpdate, Transaction
from src.config import ADMIN_USERNAME, ADMIN_PIN
from typing import List, Optional
from datetime import datetime
import hashlib
from sqlalchemy.orm import Session

# --- All functions below use SQLAlchemy ORM only ---

def create_account(db: Session, account: AccountCreate):
    hashed_pin = hashlib.sha256(account.pin.encode()).hexdigest()
    db_account = Account(
        account_number=account.account_number,
        pin=hashed_pin,
        balance=0.0
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def deposit(db: Session, account_number: str, amount: float):
    db_account = get_account(db, account_number)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    db_account.balance += amount
    transaction = Transaction(
        account_id=db_account.id,
        type="deposit",
        amount=amount
    )
    db.add(transaction)
    db.commit()
    db.refresh(db_account)
    return db_account

def withdraw(db: Session, account_number: str, amount: float):
    db_account = get_account(db, account_number)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    if db_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    db_account.balance -= amount
    transaction = Transaction(
        account_id=db_account.id,
        type="withdraw",
        amount=amount
    )
    db.add(transaction)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account(db: Session, account_number: str):
    return db.query(Account).filter(Account.account_number == account_number).first()

def get_all_accounts(db: Session):
    return db.query(Account).all()

def update_account(db: Session, account_number: str, update: AccountUpdate):
    db_account = get_account(db, account_number)
    if not db_account:
        return None
    if update.pin is not None:
        db_account.pin = hashlib.sha256(update.pin.encode()).hexdigest()
    if update.balance is not None:
        db_account.balance = update.balance
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_number: str):
    db_account = get_account(db, account_number)
    if not db_account:
        return False
    db.delete(db_account)
    db.commit()
    return True

def get_transaction_history(db: Session, account_number: str):
    db_account = get_account(db, account_number)
    if not db_account:
        return []
    return db.query(Transaction).filter(Transaction.account_id == db_account.id).all()
