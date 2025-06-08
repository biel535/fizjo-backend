from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

# Haszowanie haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sekret JWT i konfiguracja algorytmu
SECRET_KEY = "a7Wg7mhTgL9eHA"  # Upewnij się, że w produkcji jest bezpiecznie przechowywany!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """Zwraca zahaszowane hasło"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Porównuje hasło w czystej postaci z hasłem zahaszowanym"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tworzy token JWT z opcjonalnym czasem wygaśnięcia"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
