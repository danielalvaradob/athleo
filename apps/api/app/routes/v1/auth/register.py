from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserOut
from app.db.models import User, UserRole
from app.db.session import SessionLocal
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    db = SessionLocal()
    try:
        # Validate user creation logic
        if not user.is_ai_trainer and (not user.email or not user.password):
            raise HTTPException(status_code=400, detail="Email and password are required for non-AI trainers.")

        # Create a new user instance
        new_user = User(
            email=user.email,
            name=user.name,
            password_hash=user.password,  # Hash the password in a real implementation
            role=user.role,
            language=user.language,
            is_ai_trainer=user.is_ai_trainer,
        )

        # Add the user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    finally:
        db.close()