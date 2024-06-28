from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from Database.connection import mydb

router = APIRouter()


class UserProfileRequest(BaseModel):
    name: str
    email: str
    mob_num: str
    address: str
    city: str
    state: str
    pincode: str

def fetch_customer_id(email: str):
    mycursor = mydb.cursor()
    sql = "SELECT cust_id FROM Account WHERE email = %s"
    mycursor.execute(sql, (email,))
    result = mycursor.fetchone()
    mycursor.close()
    return result[0] if result else None

def check_for_profile(email: str):
    mycursor = mydb.cursor()

    # Check if email exists in Customer table
    sql_check_email = "SELECT COUNT(*) FROM Customer WHERE email = %s"
    mycursor.execute(sql_check_email, (email,))
    result = mycursor.fetchone()[0]
    mycursor.close()

    return result > 0

def insert_customer_profile_db(user_profile: UserProfileRequest, customer_id: int):
    mycursor = mydb.cursor()
    sql = "Insert INTO Customer (cust_id, name, email, mob_num, address, city, state, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (customer_id, user_profile.name, user_profile.email, user_profile.mob_num, user_profile.address, user_profile.city, user_profile.state, user_profile.pincode)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    
def update_customer_profile_db(user_profile: UserProfileRequest, customer_id: int):
    mycursor = mydb.cursor()

    # Update customer profile
    sql = "UPDATE Customer SET name = %s, email = %s, mob_num = %s, address = %s, city = %s, state = %s, pincode = %s WHERE cust_id = %s"
    val = (user_profile.name, user_profile.email, user_profile.mob_num, user_profile.address, user_profile.city, user_profile.state, user_profile.pincode, customer_id)
    mycursor.execute(sql, val)

    mydb.commit()
    mycursor.close()

    
@router.post("/com_profile")
async def update_customer_profile(user_profile: UserProfileRequest):
    # Fetch customer ID based on email
    customer_id = fetch_customer_id(user_profile.email)

    if not customer_id:
        return {"status_code":404, "detail":"Customer not found"}
    
    if check_for_profile(user_profile.email):
        update_customer_profile_db(user_profile, customer_id)
        return {"status_code": 200, "message": "Customer profile updated successfully"}
    else:
        insert_customer_profile_db(user_profile, customer_id)
        return {"status_code": 200, "message": "Customer profile created successfully"}
        
    

    





