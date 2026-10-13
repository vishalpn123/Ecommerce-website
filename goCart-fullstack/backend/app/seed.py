from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Product
PRODUCTS=[
("Studio Wireless Headphones","Immersive sound and all-day battery life.","Tech",349900,"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",25),
("Everyday Canvas Tote","Roomy durable carry-all for everyday use.","Lifestyle",89900,"https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=800",40),
("Minimal Ceramic Mug Set","Tactile ceramic mugs for slow mornings.","Home",74900,"https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800",35),
("Active Move Smartwatch","Activity tracking and a crisp display.","Tech",429900,"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",18),
("Cloud Knit Sneakers","Lightweight everyday sneakers with a cushioned feel.","Fashion",219900,"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",22),
("Botanical Desk Planter","A compact planter for your workspace.","Home",59900,"https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800",50),
("Pocket Bluetooth Speaker","Big sound in a compact speaker.","Tech",159900,"https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800",30),
("Daily Ritual Water Bottle","Reusable bottle with a leak-resistant lid.","Lifestyle",69900,"https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800",45)]
def seed_products(db:Session):
    if db.scalar(select(Product.id).limit(1)) is None:
        db.add_all([Product(name=n,description=d,category=c,price_paise=p,image_url=i,stock=s) for n,d,c,p,i,s in PRODUCTS]); db.commit()
