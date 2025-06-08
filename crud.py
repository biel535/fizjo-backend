from sqlalchemy.orm import Session
from auth import hash_password, verify_password
from models import Appointment, User
from schemas import AppointmentCreate, UserCreate
from fastapi import HTTPException


def create_user(db: Session, user: UserCreate):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email już zarejestrowany.")

    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,   # <-- koniecznie!
        role=user.role if hasattr(user, 'role') else 'user'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_appointment(db: Session, appointment: AppointmentCreate):
    # Sprawdzenie, czy istnieje już taka wizyta
    existing = db.query(Appointment).filter(
        Appointment.appointment_datetime == appointment.appointment_datetime
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ten termin jest już zajęty.")

    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()


def delete_appointment(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Wizyta nie została znaleziona.")

    db.delete(appointment)
    db.commit()
    return {"detail": "Wizyta została usunięta."}
