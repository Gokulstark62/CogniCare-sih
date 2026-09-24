from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..auth import get_current_user
from ..schemas import MedicineCreate, MedicineUpdate, MedicineOut

router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.get("", response_model=list[MedicineOut])
def list_medicines(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Medicine)
        .filter(models.Medicine.user_id == current_user.id)
        .order_by(models.Medicine.time_hour, models.Medicine.time_minute)
        .all()
    )


@router.post("", response_model=MedicineOut, status_code=status.HTTP_201_CREATED)
def create_medicine(
    payload: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    med = models.Medicine(
        user_id=current_user.id,
        name=payload.name,
        dosage=payload.dosage,
        purpose=payload.purpose,
        time_hour=payload.time_hour,
        time_minute=payload.time_minute,
    )
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.put("/{med_id}", response_model=MedicineOut)
def update_medicine(
    med_id: int,
    payload: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    med = (
        db.query(models.Medicine)
        .filter(
            models.Medicine.id == med_id,
            models.Medicine.user_id == current_user.id,
        )
        .first()
    )
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")

    if payload.name is not None:
        med.name = payload.name
    if payload.dosage is not None:
        med.dosage = payload.dosage
    if payload.purpose is not None:
        med.purpose = payload.purpose
    if payload.time_hour is not None:
        med.time_hour = payload.time_hour
    if payload.time_minute is not None:
        med.time_minute = payload.time_minute

    db.commit()
    db.refresh(med)
    return med


@router.delete("/{med_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(
    med_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    med = (
        db.query(models.Medicine)
        .filter(
            models.Medicine.id == med_id,
            models.Medicine.user_id == current_user.id,
        )
        .first()
    )
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    db.delete(med)
    db.commit()


@router.post("/{med_id}/toggle", response_model=MedicineOut)
def toggle_medicine(
    med_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    med = (
        db.query(models.Medicine)
        .filter(
            models.Medicine.id == med_id,
            models.Medicine.user_id == current_user.id,
        )
        .first()
    )
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")

    med.taken = not med.taken
    db.commit()
    db.refresh(med)
    return med