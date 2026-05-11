from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.security import create_access_token, get_current_user
from app.users import authenticate_user

app = FastAPI(title="auth-service", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}


@app.post("/v1/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Exchange username + password for a JWT token.

    This endpoint is PUBLIC — the gateway must not require a token to reach it.
    It uses OAuth2PasswordRequestForm, which expects form-encoded body:
        username=testuser&password=password

    curl example:
        curl -X POST http://localhost:8005/v1/auth/token \\
          -d "username=testuser&password=password"
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/v1/auth/me")
async def me(current_user: dict = Depends(get_current_user)):
    """
    Return the contents of the current user's token.

    Protected by get_current_user — requires a valid Bearer token.
    Use this to verify your implementation of create_access_token and get_current_user.

    curl example:
        TOKEN=$(curl -s -X POST http://localhost:8005/v1/auth/token \\
          -d "username=testuser&password=password" | jq -r .access_token)
        curl http://localhost:8005/v1/auth/me -H "Authorization: Bearer $TOKEN"
    """
    return current_user
