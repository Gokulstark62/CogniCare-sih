from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..auth import get_current_user
from ..schemas import RoutineCreate, RoutineUpdate, RoutineOut

router = APIRouter(prefix="/routine", tags=["routine"])


@router.get("", response_model=list[RoutineOut])
def list_activities(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.RoutineActivity)
        .filter(models.RoutineActivity.user_id == current_user.id)
        .order_by(
            models.RoutineActivity.time_hour,
            models.RoutineActivity.time_minute,
        )
        .all()
    )


@router.post("", response_model=RoutineOut, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: RoutineCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    act = models.RoutineActivity(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        time_hour=payload.time_hour,
        time_minute=payload.time_minute,
        icon_code_point=payload.icon_code_point,
    )
    db.add(act)
    db.commit()
    db.refresh(act)
    return act


@router.put("/{act_id}", response_model=RoutineOut)
def update_activity(
    act_id: int,
    payload: RoutineUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    act = (
        db.query(models.RoutineActivity)
        .filter(
            models.RoutineActivity.id == act_id,
            models.RoutineActivity.user_id == current_user.id,
        )
        .first()
    )
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")

    if payload.name is not None:
        act.name = payload.name
    if payload.description is not None:
        act.description = payload.description
    if payload.time_hour is not None:
        act.time_hour = payload.time_hour
    if payload.time_minute is not None:
        act.time_minute = payload.time_minute
    if payload.icon_code_point is not None:
        act.icon_code_point = payload.icon_code_point

    db.commit()
    db.refresh(act)
    return act


@router.delete("/{act_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    act_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    act = (
        db.query(models.RoutineActivity)
        .filter(
            models.RoutineActivity.id == act_id,
            models.RoutineActivity.user_id == current_user.id,
        )
        .first()
    )
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(act)
    db.commit()