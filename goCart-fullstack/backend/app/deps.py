from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import decode_subject
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    sub=decode_subject(token)
    if not sub: raise HTTPException(401,"Invalid or expired token",headers={"WWW-Authenticate":"Bearer"})
    user=db.get(User,int(sub))
    if not user: raise HTTPException(401,"User no longer exists")
    return user
def get_admin_user(user:User=Depends(get_current_user)):
    if not user.is_admin: raise HTTPException(403,"Administrator access required")
    return user
