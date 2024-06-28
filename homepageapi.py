from fastapi import APIRouter, Depends, HTTPException
from Database.connection import mydb
from typing import List
import random

router = APIRouter()

def fetch_categories():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT category_id, category_name, image_url FROM category")
    categories = cursor.fetchall()
    return categories

def fetch_random_items():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT item_id, item_name, price, unit, available_units, image_url FROM item ORDER BY RAND() LIMIT 10")
    random_items = cursor.fetchall()
    cursor.close()
    return random_items

@router.get("/category")
def category_page_data():
    # Fetch category list
    categories = fetch_categories()
    new_arrivals = fetch_random_items()
    return {"categories": categories, "new_arrivals": new_arrivals}

@router.get("/homepage")
def get_homepage_data():
    # Fetch category list
    categories = fetch_categories()

    # Fetch random 10 items
    item_list1 = fetch_random_items()
    
    # Fetch random 10 items
    item_list2 = fetch_random_items()
    return {"categories": categories, "items_list1": item_list1, "items_list2" : item_list2}
