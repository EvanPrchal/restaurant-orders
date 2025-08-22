from sqlmodel import Relationship, Field, SQLModel

class OrderItem(SQLModel, table=True):
    order_id: int | None = Field(foreign_key="order.id", primary_key=True)
    menu_number: int | None = Field(foreign_key="menuitem.menu_number", primary_key=True)

class MenuItem(SQLModel, table=True):
    menu_number: int = Field(primary_key=True)
    name: str
    price: str
    calories: int
    orders: list["Order"] = Relationship(back_populates="items", link_model=OrderItem)

class Customer(SQLModel, table=True):
    id: int| None = Field( primary_key=True)
    name: str
    orders: list["Order"] = Relationship(back_populates="customer")

class Order(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    items: list[MenuItem] = Relationship(back_populates="orders", link_model=OrderItem)
    status: str

    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="orders")