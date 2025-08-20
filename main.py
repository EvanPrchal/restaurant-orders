from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import Session, select

from database import get_db

from models import MenuItem, Customer, OrderItem, Order
from schemas import CreateMenuItemRequest, CreateCustomerRequest, UpdateMenuItemRequest, UpdateCustomerRequest


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

@app.get("/customers")
async def get_customers(db: Session = Depends(get_db)) -> list[Customer]:
    return db.exec(select(Customer)).all()

@app.get("/orders")
async def get_orders(db: Session = Depends(get_db)) -> list[Order]:
    return db.exec(select(Order)).all()

@app.get("/order_items")
async def get_order_items(db: Session = Depends(get_db)) -> list[OrderItem]:
    return db.exec(select(OrderItem)).all()

### POST ###

@app.post("/menu", status_code=status.HTTP_201_CREATED)
async def create_menu_item(create_menu_item_request: CreateMenuItemRequest, db: Session = Depends(get_db)) -> int:
    menu_item: MenuItem = MenuItem(**create_menu_item_request.model_dump())
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item.menu_number

@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(create_customer_request: CreateCustomerRequest, db: Session = Depends(get_db)) -> int:
    customer: Customer = Customer(**create_customer_request.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer.id

### PATCH ###

@app.patch("/menu/{menu_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_menu_item(menu_number: int, update_menu_item_request: UpdateMenuItemRequest, db: Session = Depends(get_db)) -> None:
    menu_item: MenuItem | None = db.get(MenuItem, menu_number)
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item number: {menu_number} does not exist.")
    for k, v in update_menu_item_request.model_dump(exclude_unset=True).items():
        setattr(menu_item, k, v)
    db.commit()
    return None

@app.patch("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_customer(customer_id: int, update_customer_request: UpdateCustomerRequest, db: Session = Depends(get_db)) -> None:
    customer: Customer | None = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer with id: {customer_id} does not exist.")
    for k, v in update_customer_request.model_dump(exclude_unset=True).items():
        setattr(customer, k, v)
    db.commit()
    return None

### DELETE ###

@app.delete("/menu/{menu_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(menu_number: int, db: Session = Depends(get_db)) -> None:
    menu_item: MenuItem | None = db.get(MenuItem, menu_number)
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item number: {menu_number} does not exist.")
    db.delete(menu_item)
    db.commit()
    return None

@app.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    customer: Customer | None = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer with id: {customer_id} does not exist.")
    db.delete(customer)
    db.commit()
    return None