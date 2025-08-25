from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import Session, select
from sqlalchemy import func
from database import get_db

from models import MenuItem, Customer, OrderItem, Order
from schemas import CreateMenuItemRequest, CreateCustomerRequest, CreateOrderRequest , UpdateMenuItemRequest, UpdateCustomerRequest, UpdateOrderRequest, GetOrderResponse, BestsellerRequest


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
async def get_orders(db: Session = Depends(get_db)) -> list[GetOrderResponse]:
    order_list: list[GetOrderResponse] = []
    orders: list[Order] | None = db.exec(select(Order)).all()
    for order in orders:
        order_list.append(GetOrderResponse(id=order.id, customer_id = order.customer_id, status=order.status, items=order.items))
    return order_list
 
@app.get("/order_items")
async def get_order_items(db: Session = Depends(get_db)) -> list[OrderItem]:
    return len(db.exec(select(OrderItem)).all())


## REPORTS ##
@app.get("/revenue")
async def get_revenue(db: Session = Depends(get_db)) -> list[GetOrderResponse]:
   #not working as of now
   return db.exec(select(GetOrderResponse)).all() 

@app.get("/menu/bestsellers")
async def get_bestsellers(db: Session = Depends(get_db)) -> list[BestsellerRequest]:
    #i know <select count(menu_number) amount_ordered FROM "orderitem" group by menu_number;> works for sql i just dont know how to do it in python </3
    return db.exec(select(func.count(MenuItem.menu_number).label("amount_ordered"), MenuItem.menu_number).select_from(OrderItem).join(MenuItem, OrderItem.menu_number == MenuItem.menu_number).group_by(MenuItem.menu_number)).all()


@app.get("/orders/{customer_id}")
async def get_number_of_customer_orders(customer_id: int, db: Session = Depends(get_db)) -> list[OrderItem]:
    #not working as of now
    return db.exec(select(Order).where(Customer.id==customer_id))
        
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

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order_with_items(create_order_request: CreateOrderRequest, db: Session = Depends(get_db)) -> int:
    items_list = []
    if db.get(Customer, create_order_request.customer_id) == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id: {create_order_request.customer_id} not found")
    for item in create_order_request.menuitems:
       if db.get(MenuItem, item):
           menu_item = db.get(MenuItem, item)
           items_list.append(menu_item)
    order: Order = Order(items=items_list, status="Placed", customer_id=create_order_request.customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order.id
    
    
### PATCH ###

@app.patch("/menu/{menu_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_menu_item(menu_number: int, update_menu_item_request: UpdateMenuItemRequest, db: Session = Depends(get_db)) -> None:
    menu_item: MenuItem | None = db.get(MenuItem, menu_number)
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item number: {menu_number} does not exist.")
    for k, v in update_menu_item_request.model_dump(exclude_unset=True).items():
        setattr(menu_item, k, v)
    db.commit()
    return None

@app.patch("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_customer(customer_id: int, update_customer_request: UpdateCustomerRequest, db: Session = Depends(get_db)) -> None:
    customer: Customer | None = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id: {customer_id} does not exist.")
    for k, v in update_customer_request.model_dump(exclude_unset=True).items():
        setattr(customer, k, v)
    db.commit()
    return None

@app.patch("/orders/{id}/status")
async def update_order_status(order_id: int, update_order_request: UpdateOrderRequest, db: Session = Depends(get_db)) -> None:
    order: Order | None = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: {order_id} does not exist.")
    for k, v in update_order_request.model_dump(exclude_unset=True).items():
        setattr(order, k, v)
        db.commit()
        return None

### DELETE ###

@app.delete("/menu/{menu_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(menu_number: int, db: Session = Depends(get_db)) -> None:
    menu_item: MenuItem | None = db.get(MenuItem, menu_number)
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item number: {menu_number} does not exist.")
    db.delete(menu_item)
    db.commit()
    return None

@app.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    customer: Customer | None = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id: {customer_id} does not exist.")
    db.delete(customer)
    db.commit()
    return None