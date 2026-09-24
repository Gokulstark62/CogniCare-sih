from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..auth import get_current_user
from ..schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentOut])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.user_id == current_user.id)
        .order_by(models.Appointment.date_time)
        .all()
    )


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    appt = models.Appointment(
        user_id=current_user.id,
        doctor_name=payload.doctor_name,
        specialty=payload.specialty,
        date_time=payload.date_time,
        location=payload.location,
        notes=payload.notes,
        icon_code_point=payload.icon_code_point,
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.put("/{appt_id}", response_model=AppointmentOut)
def update_appointment(
    appt_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    appt = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.id == appt_id,
            models.Appointment.user_id == current_user.id,
        )
        .first()
    )
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if payload.doctor_name is not None:
        appt.doctor_name = payload.doctor_name
    if payload.specialty is not None:
        appt.specialty = payload.specialty
    if payload.date_time is not None:
        appt.date_time = payload.date_time
    if payload.location is not None:
        appt.location = payload.location
    if payload.notes is not None:
        appt.notes = payload.notes
    if payload.icon_code_point is not None:
        appt.icon_code_point = payload.icon_code_point

    db.commit()
    db.refresh(appt)
    return appt


@router.delete("/{appt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appt_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    appt = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.id == appt_id,
            models.Appointment.user_id == current_user.id,
        )
        .first()
    )
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()