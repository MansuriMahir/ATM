import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.models.account import AccountSchema, AccountCreate, AccountUpdate, TransactionSchema
from src.services.atm_service import (
    get_account, create_account, get_all_accounts, update_account, delete_account,
    deposit, withdraw, get_transaction_history
)
from src.database import get_db
from typing import List

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountSchema])
def list_accounts(db: Session = Depends(get_db)):
    """Get all accounts"""
    return get_all_accounts(db)

@router.get("/{account_number}", response_model=AccountSchema)
def get_account_api(account_number: str, db: Session = Depends(get_db)):
    """Get account details by account number"""
    acc = get_account(db, account_number)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc

@router.post("/", response_model=AccountSchema)
def create_account_api(account: AccountCreate, db: Session = Depends(get_db)):
    """Create a new account"""
    return create_account(db, account)

@router.put("/{account_number}", response_model=AccountSchema)
def update_account_api(account_number: str, update: AccountUpdate, db: Session = Depends(get_db)):
    """Update account details"""
    acc = update_account(db, account_number, update)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found or no fields to update")
    return acc

@router.delete("/{account_number}")
def delete_account_api(account_number: str, db: Session = Depends(get_db)):
    """Delete an account"""
    deleted = delete_account(db, account_number)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted"}

@router.post("/{account_number}/deposit", response_model=AccountSchema)
def deposit_api(account_number: str, amount: float, db: Session = Depends(get_db)):
    """Deposit money into an account"""
    return deposit(db, account_number, amount)

@router.post("/{account_number}/withdraw", response_model=AccountSchema)
def withdraw_api(account_number: str, amount: float, db: Session = Depends(get_db)):
    """Withdraw money from an account"""
    return withdraw(db, account_number, amount)

@router.get("/{account_number}/transactions", response_model=List[TransactionSchema])
def get_transactions_api(account_number: str, db: Session = Depends(get_db)):
    """Get transaction history for an account"""
    if not get_account(db, account_number):
        raise HTTPException(status_code=404, detail="Account not found")
    return get_transaction_history(db, account_number)