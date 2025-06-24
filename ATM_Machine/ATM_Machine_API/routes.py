from fastapi import APIRouter, HTTPException, Depends
from .database import get_db
from .models import User, UserCreate, Transaction
from . import crud
from typing import List
from flask import Flask, render_template, request, redirect, url_for, session, flash
from ATM_Machine.atm_utils import get_user, create_user, update_user_balance, get_db_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"

router = APIRouter()

@router.get("/users/{account_number}", response_model=User)
def read_user(account_number: str, db=Depends(get_db)):
    user = crud.get_user(db, account_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[User])
def read_users(db=Depends(get_db)):
    return crud.get_all_users(db)

@router.post("/users", response_model=User)
def create_new_user(user: UserCreate, db=Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/transactions/{account_number}", response_model=List[Transaction])
def read_transactions(account_number: str, db=Depends(get_db)):
    return crud.get_transactions(db, account_number)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        account_number = request.form["account_number"]
        pin = request.form["pin"]
        user = get_user(account_number)
        if user and user["pin"] == pin:
            session["user"] = account_number
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    user = get_user(session["user"])
    return render_template("dashboard.html", user=user)

# Add more routes for withdraw, deposit, etc.

if __name__ == "__main__":
    app.run(debug=True)
