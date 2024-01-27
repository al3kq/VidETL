from fastapi import FastAPI, Depends, APIRouter, HTTPException, Body, File, UploadFile
from fastapi import HTTPException, Request, status
import jwt

SECRET_KEY = "DEVJWTSECRET"  # Replace with your actual key

ALGORITHM = "HS256"


def token_validator(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token not found or invalid")
    token = token[7:].strip('"')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
    print(payload)
    return payload