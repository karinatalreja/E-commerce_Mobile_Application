from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Database.connection import mydb

router = APIRouter()


class ItemDetailsResponse(BaseModel):
    item_id: str
    item_name: str
    price: float
    unit: str
    available_units: int
    image_url: str
    rating: int
    description: str
    status: str

def update_item_status(item_id: str):
    mycursor = mydb.cursor()
    sql = "UPDATE item SET status = 'out_of_stock' WHERE item_id = %s AND available_units = 0"
    mycursor.execute(sql, (item_id,))
    mydb.commit()
    mycursor.close()
    
def fetch_item_details(item_id: str):
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT item_id, item_name, price, unit, available_units, image_url, rating, description,status FROM item WHERE item_id = %s"
    mycursor.execute(sql, (item_id,))
    item_details = mycursor.fetchone()
    mycursor.close()
    return item_details

@router.get("/item_details/{item_id}")
async def get_item_details(item_id: str):
    update_item_status(item_id)
    # Fetch item details from the database based on item_id
    item_details = fetch_item_details(item_id)

    if not item_details:
        raise HTTPException(status_code=404, detail="Item not found")

    return item_details



