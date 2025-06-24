from fastapi import FastAPI, HTTPException, Depends
from .routes import router
from ATM_Machine.atm_utils import get_db_connection, create_tables

app = FastAPI(title="ATM Machine API", version="1.0.0")
app.include_router(router, prefix="/api")

@app.get("/")
def home():
    return {"message": "ATM Machine API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(dict(user))
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully!")
    list_users()

# Run the application using the command:
# cd ATM
# .venv\Scripts\uvicorn.exe ATM_Machine.ATM_Machine_API.main:app --reload
# or if uvicorn is installed globally:
# uvicorn ATM_Machine.ATM_Machine_API.main:app --reload