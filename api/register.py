## IMPORTS ##
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from Database.connection import mydb

router = APIRouter()

# Model for user registration request
class UserRegistrationRequest(BaseModel):
    name: str
    email: str
    password: str

# Model for OTP generation request
class OTPGenerationRequest(BaseModel):
    email: str

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send email with OTP
def send_otp_email(email: str, otp: str):
    # Email configuration (replace with your SMTP server details)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ShopSphere.Verify'
    smtp_password = 'bcqk llco kqsk nxdy'

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = 'shopsphere.verify@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Email Verification by ShopSphere'

    # Generate OTP message
    otp_message = f'Welcome to ShopSphere!\n\nYour OTP for registration is: {otp}\n\n\nThanks!\n\nRegards,\nShopSphere :)'

    # Attach message to email
    msg.attach(MIMEText(otp_message, 'plain'))

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

@router.post("/otp")
async def register_user(user_request: UserRegistrationRequest):
    #generate otp
    otp = generate_otp()

    # Send OTP to the registered email
    send_otp_email(user_request.email, otp)
    # Return success response
    return {"status_code": 200, "otp": otp,  "message": "OTP sent to email."}


@router.post("/register")
async def register_user(user_request: UserRegistrationRequest):
    mycursor = mydb.cursor()
    sql = "INSERT INTO Account(name, email,password) VALUES (%s, %s, %s)"
    val = (user_request.name, user_request.email, user_request.password)
    mycursor.execute(sql, val)
    mydb.commit()
    customer_id = mycursor.lastrowid  # Fetch the customer ID after committing
    print(mycursor.rowcount, "record inserted. Customer ID:", customer_id)
    return {"status_code": 200, "message": "Customer Registered Successfully!.", "cust_id": customer_id, "name": user_request.name, "email" : user_request.email}
