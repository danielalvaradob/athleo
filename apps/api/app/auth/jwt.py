from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "YOUR_SECRET_KEY"  # Cambia esto en producción (usa env)
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)