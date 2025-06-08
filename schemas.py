from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# 👤 Baza użytkownika wspólna dla Create/Out
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "pacjent"  # domyślnie pacjent


# ✍️ Używane przy rejestracji użytkownika
class UserCreate(UserBase):
    password: str


# 📤 Dane zwracane na zewnątrz (np. w odpowiedzi API)
class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 (jeśli masz v1, użyj orm_mode = True)


# 📅 Tworzenie wizyty
class AppointmentCreate(BaseModel):
    name: str
    email: str
    appointment_datetime: datetime


# 📤 Dane wizyty wysyłane na zewnątrz
class AppointmentOut(BaseModel):
    id: int
    name: str
    email: str
    appointment_datetime: datetime

    class Config:
        from_attributes = True
