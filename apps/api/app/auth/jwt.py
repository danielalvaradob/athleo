from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings

# Create an access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Create a refresh token
def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Decode a token
def decode_token(token: str, secret_key: str):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return decoded
    except JWTError:
        raise Exception("Invalid or expired token")