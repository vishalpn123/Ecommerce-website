from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    is_admin: Mapped[bool]=mapped_column(Boolean,default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Product(Base):
    __tablename__="products"
    id: Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str]=mapped_column(String(180),index=True)
    description: Mapped[str]=mapped_column(Text,default="")
    category: Mapped[str]=mapped_column(String(80),index=True)
    price_paise: Mapped[int]=mapped_column(Integer)
    image_url: Mapped[str]=mapped_column(String(1000),default="")
    stock: Mapped[int]=mapped_column(Integer,default=0)
    active: Mapped[bool]=mapped_column(Boolean,default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class CartItem(Base):
    __tablename__="cart_items"
    __table_args__=(UniqueConstraint("user_id","product_id",name="uq_cart_user_product"),)
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id",ondelete="CASCADE"),index=True)
    quantity: Mapped[int]=mapped_column(Integer,default=1)
class Order(Base):
    __tablename__="orders"
    id: Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    status: Mapped[str]=mapped_column(String(30),default="pending_payment")
    total_paise: Mapped[int]=mapped_column(Integer)
    shipping_name: Mapped[str]=mapped_column(String(100))
    shipping_address: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class OrderItem(Base):
    __tablename__="order_items"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey("orders.id",ondelete="CASCADE"),index=True)
    product_id: Mapped[int]=mapped_column(Integer)
    product_name: Mapped[str]=mapped_column(String(180))
    unit_price_paise: Mapped[int]=mapped_column(Integer)
    quantity: Mapped[int]=mapped_column(Integer)
