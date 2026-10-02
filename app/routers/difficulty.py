from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..auth import get_current_user
from ..schemas import DifficultyOut, DifficultyUpdate

router = APIRouter(prefix="/difficulty", tags=["difficulty"])


def _get_or_create(db: Session, user_id: int) -> models.GameDifficulty:
    row = (
        db.query(models.GameDifficulty)
        .filter(models.GameDifficulty.user_id == user_id)
        .first()
    )
    if not row:
        row = models.GameDifficulty(user_id=user_id)
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


@router.get("", response_model=DifficultyOut)
def get_difficulty(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return _get_or_create(db, current_user.id)


@router.post("", response_model=DifficultyOut)
def set_difficulty(
    payload: DifficultyUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    row = _get_or_create(db, current_user.id)
    row.memory_match_level = payload.memory_match_level
    row.word_builder_level = payload.word_builder_level
    row.picture_level = payload.picture_level
    row.number_seq_level = payload.number_seq_level
    db.commit()
    db.refresh(row)
    return row