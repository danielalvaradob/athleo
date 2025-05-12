# app/routes/v1/user.py

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserOut
from app.db.models import User, UserRole
from app.db.session import SessionLocal
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users")

def get_user_by_id(user_id: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    finally:
        db.close()

@router.post("/create-ai", response_model=UserOut)
def create_ai_user(user: UserCreate, admin_user_id: str = Depends(get_user_by_id)):
    db = SessionLocal()
    try:
        # Validate if the admin_user_id belongs to an admin
        admin_user = db.query(User).filter(User.id == admin_user_id).first()
        if not admin_user or admin_user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Only admins can create AI trainers.")

        # Ensure the user being created is an AI trainer
        if not user.is_ai_trainer:
            raise HTTPException(status_code=400, detail="Only AI trainers can be created through this route.")

        # Create a new AI trainer instance
        new_ai_user = User(
            email=None,  # AI trainers do not have an email
            name=user.name,
            password_hash=None,  # AI trainers do not have a password
            role=UserRole.trainer,
            language=user.language,
            is_ai_trainer=True,
        )

        # Add the AI trainer to the database
        db.add(new_ai_user)
        db.commit()
        db.refresh(new_ai_user)

        return new_ai_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="An error occurred while creating the AI trainer.")
    finally:
        db.close()