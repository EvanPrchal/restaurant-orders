from pydantic import BaseModel
from models import MenuItem
class GetOrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    items: list[MenuItem]

class CreateMenuItemRequest(BaseModel):
    name: str
    price: str
    calories: int

class CreateCustomerRequest(BaseModel):
    name: str

class CreateOrderRequest(BaseModel):
    customer_id: int
    menuitems: list[int]

class UpdateMenuItemRequest(BaseModel):
    name: str
    price: str
    calories: int

class UpdateCustomerRequest(BaseModel):
    name: str

class UpdateOrderRequest(BaseModel):
    status: str