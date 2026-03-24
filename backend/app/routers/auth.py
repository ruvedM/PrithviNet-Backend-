from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.services import auth_service
from app.services.auth_service import register_user


# TODO: Create app.database and implement get_db
try:
    from app.database import get_db
except ImportError:
    # Placeholder to avoid import error during initialization
    def get_db():
        yield None

# TODO: Create app.schemas.auth_schema
# TODO: Create app.services.auth_service
# TODO: Create app.core.security

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/login", status_code=status.HTTP_200_OK)
async def login_page():
    """
    Returns login page metadata or status.
    """
    return {"message": "Login endpoint. Use POST to authenticate."}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(db, data)

@router.get("/register", status_code=status.HTTP_200_OK)
async def register_page():
    """
    Returns registration page metadata or status.
    """
    return {"message": "Registration endpoint. Use POST to create an account."}

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)

@router.get("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password_page():
    """
    Returns forgot password page metadata or status.
    """
    return {"message": "Forgot password endpoint. Use POST to request a reset link."}

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(db: Session = Depends(get_db)):
    """
    Handles forgot password request and sends a reset link.
    """
    # TODO: Implement business logic using app.services.auth_service
    return {"message": "Password reset link sent if email exists"}

@router.get("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_page():
    """
    Returns reset password page metadata or status.
    """
    return {"message": "Reset password endpoint. Use PUT to update your password."}

@router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(db: Session = Depends(get_db)):
    """
    Resets the user's password.
    """
    # TODO: Implement business logic using app.services.auth_service
    return {"message": "Password reset successful"}
