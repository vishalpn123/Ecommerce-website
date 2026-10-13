from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select,or_
from sqlalchemy.orm import Session
from app.config import settings
from app.database import Base,SessionLocal,engine,get_db
from app.models import User,Product,CartItem,Order,OrderItem
from app.schemas import UserCreate,UserOut,TokenOut,LoginIn,ProductIn,ProductOut,CartAdd,CartUpdate,CartLine,CartOut,OrderCreate,OrderOut
from app.security import hash_password,verify_password,create_access_token
from app.deps import get_current_user,get_admin_user
from app.seed import seed_products
@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db: seed_products(db)
    yield
app=FastAPI(title="goCart API",version="1.0.0",description="Full-stack goCart ecommerce API",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.frontend_origins.split(",") if x.strip()],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
def cart_data(db,user_id):
    rows=db.scalars(select(CartItem).where(CartItem.user_id==user_id)).all(); lines=[]
    for row in rows:
        product=db.get(Product,row.product_id)
        if product and product.active: lines.append(CartLine(product=product,quantity=row.quantity,line_total_paise=product.price_paise*row.quantity))
    return CartOut(items=lines,subtotal_paise=sum(x.line_total_paise for x in lines),item_count=sum(x.quantity for x in lines))
@app.get("/api/health")
def health(): return {"status":"ok","service":"goCart API"}
@app.post("/api/auth/register",response_model=TokenOut,status_code=201)
def register(data:UserCreate,db:Session=Depends(get_db)):
    email=data.email.lower()
    if db.scalar(select(User).where(User.email==email)): raise HTTPException(409,"Email already registered")
    user=User(name=data.name.strip(),email=email,password_hash=hash_password(data.password)); db.add(user); db.commit(); db.refresh(user)
    return TokenOut(access_token=create_access_token(str(user.id)),user=user)
@app.post("/api/auth/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==data.email.lower()))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Incorrect email or password")
    return TokenOut(access_token=create_access_token(str(user.id)),user=user)
@app.get("/api/auth/me",response_model=UserOut)
def me(user:User=Depends(get_current_user)): return user
@app.get("/api/products",response_model=list[ProductOut])
def products(q:str|None=Query(None,max_length=100),category:str|None=None,sort:str=Query("featured",pattern="^(featured|price_asc|price_desc)$"),db:Session=Depends(get_db)):
    stmt=select(Product).where(Product.active.is_(True))
    if q:
        term=f"%{q.strip()}%"; stmt=stmt.where(or_(Product.name.ilike(term),Product.description.ilike(term),Product.category.ilike(term)))
    if category and category.lower()!="all": stmt=stmt.where(Product.category.ilike(category))
    if sort=="price_asc": stmt=stmt.order_by(Product.price_paise.asc())
    elif sort=="price_desc": stmt=stmt.order_by(Product.price_paise.desc())
    else: stmt=stmt.order_by(Product.id.asc())
    return list(db.scalars(stmt.limit(100)).all())
@app.get("/api/products/{pid}",response_model=ProductOut)
def product(pid:int,db:Session=Depends(get_db)):
    p=db.get(Product,pid)
    if not p or not p.active: raise HTTPException(404,"Product not found")
    return p
@app.post("/api/products",response_model=ProductOut,status_code=201)
def create_product(data:ProductIn,db:Session=Depends(get_db),admin:User=Depends(get_admin_user)):
    p=Product(**data.model_dump()); db.add(p); db.commit(); db.refresh(p); return p
@app.put("/api/products/{pid}",response_model=ProductOut)
def update_product(pid:int,data:ProductIn,db:Session=Depends(get_db),admin:User=Depends(get_admin_user)):
    p=db.get(Product,pid)
    if not p: raise HTTPException(404,"Product not found")
    for k,v in data.model_dump().items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return p
@app.delete("/api/products/{pid}",status_code=204)
def delete_product(pid:int,db:Session=Depends(get_db),admin:User=Depends(get_admin_user)):
    p=db.get(Product,pid)
    if not p: raise HTTPException(404,"Product not found")
    p.active=False; db.commit()
@app.get("/api/cart",response_model=CartOut)
def get_cart(db:Session=Depends(get_db),user:User=Depends(get_current_user)): return cart_data(db,user.id)
@app.post("/api/cart/items",response_model=CartOut)
def add_cart(data:CartAdd,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    p=db.get(Product,data.product_id)
    if not p or not p.active: raise HTTPException(404,"Product not found")
    row=db.scalar(select(CartItem).where(CartItem.user_id==user.id,CartItem.product_id==p.id)); qty=(row.quantity if row else 0)+data.quantity
    if qty>p.stock: raise HTTPException(409,f"Only {p.stock} units available")
    if row: row.quantity=qty
    else: db.add(CartItem(user_id=user.id,product_id=p.id,quantity=data.quantity))
    db.commit(); return cart_data(db,user.id)
@app.patch("/api/cart/items/{pid}",response_model=CartOut)
def update_cart(pid:int,data:CartUpdate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    row=db.scalar(select(CartItem).where(CartItem.user_id==user.id,CartItem.product_id==pid))
    if not row: raise HTTPException(404,"Cart item not found")
    if data.quantity==0: db.delete(row)
    else:
        p=db.get(Product,pid)
        if not p or data.quantity>p.stock: raise HTTPException(409,"Requested quantity unavailable")
        row.quantity=data.quantity
    db.commit(); return cart_data(db,user.id)
@app.delete("/api/cart/items/{pid}",response_model=CartOut)
def remove_cart(pid:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    row=db.scalar(select(CartItem).where(CartItem.user_id==user.id,CartItem.product_id==pid))
    if row: db.delete(row); db.commit()
    return cart_data(db,user.id)
@app.post("/api/orders",response_model=OrderOut,status_code=201)
def create_order(data:OrderCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    rows=db.scalars(select(CartItem).where(CartItem.user_id==user.id)).all(); valid=[]
    for row in rows:
        p=db.get(Product,row.product_id)
        if p and p.active: valid.append((row,p))
    if not valid: raise HTTPException(400,"Your cart is empty")
    for row,p in valid:
        if row.quantity>p.stock: raise HTTPException(409,f"Insufficient stock for {p.name}")
    total=sum(row.quantity*p.price_paise for row,p in valid)
    order=Order(user_id=user.id,total_paise=total,shipping_name=data.shipping_name.strip(),shipping_address=data.shipping_address.strip(),status="pending_payment")
    db.add(order); db.flush()
    for row,p in valid:
        db.add(OrderItem(order_id=order.id,product_id=p.id,product_name=p.name,unit_price_paise=p.price_paise,quantity=row.quantity)); p.stock-=row.quantity; db.delete(row)
    db.commit(); db.refresh(order)
    return {"id":order.id,"status":order.status,"total_paise":order.total_paise,"shipping_name":order.shipping_name,"shipping_address":order.shipping_address,"created_at":order.created_at,"items":db.scalars(select(OrderItem).where(OrderItem.order_id==order.id)).all()}
@app.get("/api/orders",response_model=list[OrderOut])
def orders(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    result=[]
    for order in db.scalars(select(Order).where(Order.user_id==user.id).order_by(Order.created_at.desc())).all():
        items=db.scalars(select(OrderItem).where(OrderItem.order_id==order.id)).all()
        result.append({"id":order.id,"status":order.status,"total_paise":order.total_paise,"shipping_name":order.shipping_name,"shipping_address":order.shipping_address,"created_at":order.created_at,"items":items})
    return result
