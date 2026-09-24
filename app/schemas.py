from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ─── User / Auth ────────────────────────────────
class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str
    phone: Optional[str] = None
    role: str = "caregiver"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ─── Medicine ───────────────────────────────────
class MedicineCreate(BaseModel):
    name: str
    dosage: str
    purpose: str
    time_hour: int = Field(ge=0, le=23)
    time_minute: int = Field(ge=0, le=59)


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    purpose: Optional[str] = None
    time_hour: Optional[int] = Field(default=None, ge=0, le=23)
    time_minute: Optional[int] = Field(default=None, ge=0, le=59)


class MedicineOut(BaseModel):
    id: int
    name: str
    dosage: str
    purpose: str
    time_hour: int
    time_minute: int
    taken: bool

    class Config:
        from_attributes = True


# ─── Hydration ──────────────────────────────────
class HydrationAdd(BaseModel):
    glasses: int = Field(ge=1, le=20)


class HydrationGoal(BaseModel):
    daily_goal: int = Field(ge=1, le=30)


class HydrationEntryOut(BaseModel):
    id: int
    timestamp: datetime
    glasses: int

    class Config:
        from_attributes = True


class HydrationSummary(BaseModel):
    today_total: int
    daily_goal: int
    entries: list[HydrationEntryOut]


# ─── Routine ────────────────────────────────────
class RoutineCreate(BaseModel):
    name: str
    description: str = ""
    time_hour: int = Field(ge=0, le=23)
    time_minute: int = Field(ge=0, le=59)
    icon_code_point: int


class RoutineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    time_hour: Optional[int] = Field(default=None, ge=0, le=23)
    time_minute: Optional[int] = Field(default=None, ge=0, le=59)
    icon_code_point: Optional[int] = None


class RoutineOut(BaseModel):
    id: int
    name: str
    description: str
    time_hour: int
    time_minute: int
    icon_code_point: int

    class Config:
        from_attributes = True


# ─── Appointment ────────────────────────────────
class AppointmentCreate(BaseModel):
    doctor_name: str
    specialty: str
    date_time: datetime
    location: str
    notes: str = ""
    icon_code_point: int


class AppointmentUpdate(BaseModel):
    doctor_name: Optional[str] = None
    specialty: Optional[str] = None
    date_time: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    icon_code_point: Optional[int] = None


class AppointmentOut(BaseModel):
    id: int
    doctor_name: str
    specialty: str
    date_time: datetime
    location: str
    notes: str
    icon_code_point: int

    class Config:
        from_attributes = True


# ─── Game Difficulty ────────────────────────────
class DifficultyUpdate(BaseModel):
    memory_match_level: int = Field(ge=0, le=2)
    word_builder_level: int = Field(ge=0, le=2)
    picture_level: int = Field(ge=0, le=2)
    number_seq_level: int = Field(ge=0, le=2)


class DifficultyOut(BaseModel):
    memory_match_level: int
    word_builder_level: int
    picture_level: int
    number_seq_level: int

    class Config:
        from_attributes = True