from datetime import datetime, date
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..auth import get_current_user
from ..schemas import (
    HydrationAdd,
    HydrationGoal,
    HydrationSummary,
    HydrationEntryOut,
)

router = APIRouter(prefix="/hydration", tags=["hydration"])


def _today_start() -> datetime:
    today = date.today()
    return datetime(today.year, today.month, today.day)


def _current_goal(db: Session, user_id: int) -> int:
    latest = (
        db.query(models.HydrationEntry)
        .filter(models.HydrationEntry.user_id == user_id)
        .order_by(models.HydrationEntry.timestamp.desc())
        .first()
    )
    return latest.daily_goal if latest else 8


@router.get("", response_model=HydrationSummary)
def get_hydration(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    entries = (
        db.query(models.HydrationEntry)
        .filter(
            models.HydrationEntry.user_id == current_user.id,
            models.HydrationEntry.timestamp >= _today_start(),
        )
        .order_by(models.HydrationEntry.timestamp.desc())
        .all()
    )
    today_total = sum(e.glasses for e in entries)
    return HydrationSummary(
        today_total=today_total,
        daily_goal=_current_goal(db, current_user.id),
        entries=[HydrationEntryOut.model_validate(e) for e in entries],
    )


@router.post(
    "/glass",
    response_model=HydrationEntryOut,
    status_code=status.HTTP_201_CREATED,
)
def add_glass(
    payload: HydrationAdd,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    entry = models.HydrationEntry(
        user_id=current_user.id,
        timestamp=datetime.utcnow(),
        glasses=payload.glasses,
        daily_goal=_current_goal(db, current_user.id),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.post("/goal")
def set_goal(
    payload: HydrationGoal,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    entries = (
        db.query(models.HydrationEntry)
        .filter(models.HydrationEntry.user_id == current_user.id)
        .all()
    )
    if entries:
        for e in entries:
            e.daily_goal = payload.daily_goal
        db.commit()
    else:
        entry = models.HydrationEntry(
            user_id=current_user.id,
            timestamp=datetime.utcnow(),
            glasses=0,
            daily_goal=payload.daily_goal,
        )
        db.add(entry)
        db.commit()
    return {"status": "ok", "daily_goal": payload.daily_goal}


@router.delete("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_today(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db.query(models.HydrationEntry).filter(
        models.HydrationEntry.user_id == current_user.id,
        models.HydrationEntry.timestamp >= _today_start(),
    ).delete()
    db.commit()