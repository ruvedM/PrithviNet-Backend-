from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.models.user import User
from app.schemas.auth_schema import RegisterRequest, LoginRequest


# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "prithvinet_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# -----------------------------
# Password Utilities
# -----------------------------

def hash_password(password: str):
    """Hash a user's password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Verify password with hash"""
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# Token Generator
# -----------------------------

def create_access_token(data: dict):
    """Create JWT access token"""

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# -----------------------------
# Register User
# -----------------------------

def register_user(db: Session, user_data: RegisterRequest):

    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        return {"error": "User with this email already exists"}

    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        city=user_data.city
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }


# -----------------------------
# Login User
# -----------------------------

def authenticate_user(db: Session, login_data: LoginRequest):

    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(login_data.password, user.password):
        return {"error": "Invalid password"}

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }