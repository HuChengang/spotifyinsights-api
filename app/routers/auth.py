from fastapi import APIRouter, HTTPException, status
from app.core.auth import create_access_token, DEMO_USERS
from app.schemas.schemas import Token, LoginRequest

router = APIRouter()


@router.post("/token", response_model=Token, tags=["Authentication"])
def login(credentials: LoginRequest):
    """
    Obtain a JWT access token.

    Use this token in the Authorization header as: `Bearer <token>`

    Demo credentials:
    - username: `admin`
    - password: `password123`
    """
    expected_password = DEMO_USERS.get(credentials.username)
    if not expected_password or credentials.password != expected_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(data={"sub": credentials.username})
    return {"access_token": token, "token_type": "bearer"}
