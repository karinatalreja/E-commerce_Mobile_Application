from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from Database.connection import mydb

router = APIRouter()

@router.get("/fetch_profile/{cust_id}")
async def get_customer_details(cust_id: int):
    try:
        mycursor = mydb.cursor(dictionary=True)
        # Fetch customer details from the database based on cust_id
        sql = "SELECT * FROM customer WHERE cust_id = %s"
        mycursor.execute(sql, (cust_id,))
        customer_data = mycursor.fetchone()
        mycursor.close()
        if customer_data:
            return customer_data  
        else:
            return {"status_code":404, "detail" :"Customer not found"}
    except Exception as e:
        return {"status_code": 500, "detail": str(e)}