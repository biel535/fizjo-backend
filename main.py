from fastapi import FastAPI, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud, models, schemas
from models import User
from schemas import UserCreate, UserOut
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from dependencies import require_role, get_current_user

from datetime import timedelta

# Tworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency do bazy danych
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- AUTH ---
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Nieprawidłowy email lub hasło")
    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# --- APPOINTMENTS ---
@app.post("/appointments/", response_model=schemas.AppointmentOut)
def book_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appointment)


@app.get("/appointments", response_model=list[schemas.AppointmentOut], dependencies=[Depends(require_role("fizjoterapeuta"))])
def read_appointments(db: Session = Depends(get_db)):
    return crud.get_appointments(db)


@app.delete("/appointments/{appointment_id}", dependencies=[Depends(require_role("fizjoterapeuta"))])
def remove_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return crud.delete_appointment(db, appointment_id)
