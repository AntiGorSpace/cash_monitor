import datetime
from passlib.context import CryptContext
from jose import jwt
from .config import ACCESS_TOKEN_EXPIRE_DAYS, HASH_KEY

pwd_context = CryptContext(schemes='bcrypt', deprecated="auto")

# def hash_password(password:str) -> str:
# 	return pwd_context.hash(password)

# def verify_password(password:str, hash:str) -> bool:
# 	return pwd_context.verify(password, hash)

def create_accsess_token(data: dict) -> str:
	to_encode = data.copy()
	to_encode["exp"] = datetime.datetime.utcnow()+datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
	return jwt.encode(to_encode, HASH_KEY, algorithm='HS256')

def decode_accsess_token(token: str) -> dict | None:
	try:
		encode_jwt = jwt.decode(token, HASH_KEY, algorithms='HS256')
	except:
		return None
	return encode_jwt

