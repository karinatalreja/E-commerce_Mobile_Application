from fastapi import FastAPI, Request, Response
from register import router as registration_router
from login import router as login_router
from homepageapi import router as home_page
from completeprofile import router as complete_profile
from category import router as items_by_category
from billing import router as bill
from itemdetails import router as item_details
from buy import router as place_order
from fetchprofile import router as fetch_profile

# Create the FastAPI application

app = FastAPI(title="Backend-control")

app.include_router(registration_router, prefix="/api")
app.include_router(login_router, prefix="/api")
app.include_router(home_page, prefix="/api")
app.include_router(complete_profile, prefix = "/api")
app.include_router(items_by_category, prefix="/api")
app.include_router(bill, prefix="/api")
app.include_router(item_details, prefix="/api")
app.include_router(place_order,prefix="/api")
app.include_router(fetch_profile, prefix = "/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Backend-control"}
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4090)
