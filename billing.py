from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from Database.connection import mydb
import decimal


router = APIRouter()


class OrderItem(BaseModel):
    item_id: str
    quantity: int

class OrderRequest(BaseModel):
    order: List[OrderItem]

def fetch_item_price(item_id: str):
    mycursor = mydb.cursor()
    sql = "SELECT price FROM item WHERE item_id = %s"
    mycursor.execute(sql, (item_id,))
    result = mycursor.fetchone()
    mycursor.close()
    return result[0] if result else 0

def update_available_units(item_id: str):
    mycursor = mydb.cursor()
    sql = "UPDATE item SET available_units = available_units - 1 WHERE item_id = %s"
    mycursor.execute(sql, (item_id,))
    mydb.commit()
    mycursor.close()


@router.post("/calculate_order")
async def calculate_order_total(order_data: OrderRequest):
    try:
        total_amount = decimal.Decimal(0)
        # Calculate total amount for each item
        for order_item in order_data.order:
            item_id = order_item.item_id
            quantity = order_item.quantity
            item_price = fetch_item_price(item_id)
            if item_price is None:
                raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
            total_amount += (item_price * quantity)
            update_available_units(item_id)

        # Apply 10% discount
        discount = total_amount * decimal.Decimal(0.10)
        new_total = total_amount - discount

        return {
            "status_code" : 200,
            "total_Amount": total_amount,
            "discount": "10 %",
            "total_after_discount": new_total,
            "delivery_Charge": decimal.Decimal(60),
            "total_to_pay": new_total + decimal.Decimal(60)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




