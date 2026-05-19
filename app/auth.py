import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "demo-secret"
ALGORITHM = "HS256"

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    options={"verify_aud": False}
)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("scope") != "payment":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return payload


def create_demo_token():
    payload = {
        "sub": "user-123",
        "scope": "payment",
        "iss": "corporate-idp",
        "aud": "payment-api"
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)