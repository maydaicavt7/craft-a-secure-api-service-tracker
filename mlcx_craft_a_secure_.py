Python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

app = FastAPI(title="Secure API Service Tracker")

# API Secret Key
SECRET_KEY = "mlcx_secret_key_123"
ALGORITHM = "HS256"

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User Model
class User(BaseModel):
    username: str
    email: str
    password: str

# User Database (In-memory for demonstration purposes)
users_db = {
    "john": {"username": "john", "email": "john@example.com", "password": "password123"},
    "jane": {"username": "jane", "email": "jane@example.com", "password": "password123"},
}

# API Endpoints
@app.post("/token")
async def read_users(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = jwt.encode({"username": user["username"], "email": user["email"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/trackings/{tracking_id}")
async def read_tracking(tracking_id: str, token: str = Depends(oauth2_scheme)):
    # Token verification and user authentication
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # API business logic
    if tracking_id == "123456":
        return {"tracking_id": tracking_id, "status": "delivered"}
    else:
        return {"tracking_id": tracking_id, "status": "in-transit"}

@app.post("/trackings/")
async def create_tracking(tracking_id: str, token: str = Depends(oauth2_scheme)):
    # Token verification and user authentication
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # API business logic
    return {"tracking_id": tracking_id, "status": "created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)