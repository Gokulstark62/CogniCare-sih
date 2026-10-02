from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, default="caregiver")  # "caregiver" or "elder"
    created_at = Column(DateTime, default=datetime.utcnow)


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    time_hour = Column(Integer, nullable=False)     # 0-23
    time_minute = Column(Integer, nullable=False)   # 0-59
    taken = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class HydrationEntry(Base):
    __tablename__ = "hydration_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    glasses = Column(Integer, nullable=False)
    daily_goal = Column(Integer, default=8)


class RoutineActivity(Base):
    __tablename__ = "routine_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    time_hour = Column(Integer, nullable=False)
    time_minute = Column(Integer, nullable=False)
    icon_code_point = Column(Integer, nullable=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    notes = Column(String, default="")
    icon_code_point = Column(Integer, nullable=False)


class GameDifficulty(Base):
    __tablename__ = "game_difficulty"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    memory_match_level = Column(Integer, default=0)
    word_builder_level = Column(Integer, default=0)
    picture_level = Column(Integer, default=0)
    number_seq_level = Column(Integer, default=0)