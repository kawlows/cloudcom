# backend/app/routers/customers.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_active_user

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/me", response_model=schemas.UserRead)
def get_me(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return current_user


@router.put("/me", response_model=schemas.UserRead)
def update_me(
    user_in: schemas.UserBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    current_user.full_name = user_in.full_name
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user