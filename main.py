from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import Session, select

from database import get_db

from models import MenuItem, Customer, OrderItem, Order



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_methods=["*"],
     allow_headers=["*"],
)

### GET ###

@app.get("/menu")
async def get_menu(db: Session = Depends(get_db)) -> list[MenuItem]:
    return db.exec(select(MenuItem)).all()

### POST ###

### PATCH ###

### DELETE ###