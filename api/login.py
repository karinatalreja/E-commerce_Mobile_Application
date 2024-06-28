## IMPORTS ##
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from Database.connection import mydb

router = APIRouter()

class User(BaseModel):
    cust_id: int
    name: str
    email: str

# Model for login request
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login_user(login_request: LoginRequest):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM Account WHERE email = %s"
    val = (login_request.email,)
    mycursor.execute(sql, val)
    account = mycursor.fetchone()

    if account:
        cust_id, name, email, db_password = account
        if login_request.password == db_password:
            # Password is correct
            return {"status_code": 200, "message": "Login successful!", "user_id": cust_id, "name": name, "email": email}
        else:
            # Password is incorrect
            raise HTTPException(status_code=401, detail="Incorrect email or password")
    else:
        # User not found
        raise HTTPException(status_code=401, detail="User not found")
