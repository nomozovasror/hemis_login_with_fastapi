import os
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        employee_id: str = payload.get("sub")
        roles: list = payload.get("roles")
        if employee_id is None or roles is None:
            raise credentials_exception
        return {'employee_id': employee_id, 'roles': roles}
    except JWTError:
        raise credentials_exception

def admin_required(current_user: dict = Depends(get_current_user)):
    if 'admin' not in current_user['roles']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return current_user

