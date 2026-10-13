from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
class UserCreate(BaseModel):
    name: str=Field(min_length=2,max_length=100); email: EmailStr; password: str=Field(min_length=8,max_length=128)
class UserOut(BaseModel):
    id:int; name:str; email:EmailStr; is_admin:bool
    model_config=ConfigDict(from_attributes=True)
class TokenOut(BaseModel): access_token:str; token_type:str="bearer"; user:UserOut
class LoginIn(BaseModel): email:EmailStr; password:str
class ProductIn(BaseModel):
    name:str=Field(min_length=2,max_length=180); description:str=Field(default="",max_length=5000); category:str=Field(min_length=2,max_length=80); price_paise:int=Field(gt=0); image_url:str=Field(default="",max_length=1000); stock:int=Field(default=0,ge=0)
class ProductOut(BaseModel):
    id:int; name:str; description:str; category:str; price_paise:int; image_url:str; stock:int; active:bool
    model_config=ConfigDict(from_attributes=True)
class CartAdd(BaseModel): product_id:int; quantity:int=Field(default=1,ge=1,le=99)
class CartUpdate(BaseModel): quantity:int=Field(ge=0,le=99)
class CartLine(BaseModel): product:ProductOut; quantity:int; line_total_paise:int
class CartOut(BaseModel): items:list[CartLine]; subtotal_paise:int; item_count:int
class OrderCreate(BaseModel): shipping_name:str=Field(min_length=2,max_length=100); shipping_address:str=Field(min_length=8,max_length=1000)
class OrderItemOut(BaseModel):
    id:int; product_id:int; product_name:str; unit_price_paise:int; quantity:int
    model_config=ConfigDict(from_attributes=True)
class OrderOut(BaseModel):
    id:int; status:str; total_paise:int; shipping_name:str; shipping_address:str; created_at:datetime; items:list[OrderItemOut]
