from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Database.connection import mydb

router = APIRouter()


class CategoryName(BaseModel):
    category_name: str


def fetch_category_id(category_name: str):
    mycursor = mydb.cursor()
    sql = "SELECT category_id FROM category WHERE category_name LIKE %s"
    mycursor.execute(sql, ('%' + category_name + '%',))
    result = mycursor.fetchone()
    mycursor.close()
    return result[0] if result else None

def fetch_items_by_category_id(category_id: int):
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT item_id, item_name, price, unit, available_units, image_url FROM item WHERE category_id = %s"
    mycursor.execute(sql, (category_id,))
    items = mycursor.fetchall()
    mycursor.close()
    return items

@router.post("/items_by_category")
async def get_items_by_category(category_data: CategoryName):
    category_name = category_data.category_name

    # Fetch category ID based on category name
    category_id = fetch_category_id(category_name)

    if not category_id:
        raise HTTPException(status_code=404, detail="Category not found")

    # Fetch items belonging to the category ID
    items = fetch_items_by_category_id(category_id)

    return {"data": items}











