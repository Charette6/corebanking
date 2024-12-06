SECRET_KEY = ""
ALGORITHM = "HS256"


def create_jwt(payload: dict, expires_in: int = 3600):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    payload["exp"] = expiration # Add expiration claim
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

@app.get("/jwt")
async def jwt_route():
    payload = {"user_id": "0ce83747-0a0b-44b0-b507-9288f150b540", "role": "admin", "scope": "dev"}
    token = create_jwt(payload)

    return [{"access_token": token}]
            
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

