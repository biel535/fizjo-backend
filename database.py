from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Wczytaj zmienne środowiskowe z .env
load_dotenv()

# Pobierz URL do bazy z .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Utwórz silnik
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Funkcja do pobierania sesji DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
