from sqlmodel import Relationship, Field, SQLModel

class OrderLinkTable(SQLModel, table=True):
    order_item_id: int | None = Field(foreign_key="orderitem.id", primary_key=True)
    order_id: int | None = Field(foreign_key="order.id", primary_key=True)


class MenuItem(SQLModel, table=True):
    menu_number: int = Field(primary_key=True)
    name: str
    price: str
    calories: int

class Customer(SQLModel, table=True):
    id: int| None = Field( primary_key=True)
    name: str
    orders: list["Order"] = Relationship(back_populates="customer")

class OrderItem(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    substitutions: str
    price: str
    orders: list["Order"] = Relationship(back_populates="items", link_model=OrderLinkTable)


class Order(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    items: list[OrderItem] = Relationship(back_populates="orders", link_model=OrderLinkTable)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="orders")
    status: str