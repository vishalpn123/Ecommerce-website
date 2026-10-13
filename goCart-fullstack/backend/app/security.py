from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from pwdlib import PasswordHash
from app.config import settings
password_hash=PasswordHash.recommended()
def hash_password(password:str)->str: return password_hash.hash(password)
def verify_password(password:str,hashed:str)->bool: return password_hash.verify(password,hashed)
def create_access_token(subject:str)->str:
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({"sub":subject,"exp":exp},settings.jwt_secret,algorithm="HS256")
def decode_subject(token:str):
    try: return jwt.decode(token,settings.jwt_secret,algorithms=["HS256"]).get("sub")
    except JWTError: return None
