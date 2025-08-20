from pydantic import BaseModel

class CreateMenuItemRequest(BaseModel):
    name: str
    price: str
    calories: int

class CreateCustomerRequest(BaseModel):
    name: str

class CreateOrderRequest(BaseModel):
    name: str
    substitutions: str
    price: str
    orders: str

class UpdateMenuItemRequest(BaseModel):
    name: str
    price: str
    calories: int

class UpdateCustomerRequest(BaseModel):
    name: str

class UpdateOrderRequest(BaseModel):
    status: str