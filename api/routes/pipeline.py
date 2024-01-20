from fastapi import FastAPI, Depends, APIRouter, HTTPException, Body
import json
from fastapi.security import OAuth2PasswordBearer
import uuid
import jwt
from functools import wraps
from typing import Optional
from ..services.json_to_pipe import json_to_pipeline

from fastapi import HTTPException, Request, status
from functools import wraps

SECRET_KEY = "DEVJWTSECRET"  # Replace with your actual key

ALGORITHM = "HS256"

def token_validator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        if request is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Request object not found")

        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token not found or invalid")

        token = token.split(" ")[1]  # Get the token part from "Bearer <token>"
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Add additional validation here if necessary (e.g., check 'sub' field in payload)
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token")

        return await func(*args, **kwargs)
    return wrapper


router = APIRouter()

# Example in-memory storage for pipelines
pipelines = {}

@router.get("/")
async def read_root():
    return {"Hello": "World"}

# In routes/pipeline.py


@router.post("/pipeline")
@token_validator
async def create_pipeline(request: Request, pipeline_data: dict = Body(...)):
    pipeline_id = str(uuid.uuid4())
    try:
        # Extract the pipeline configuration and output directory
        pipeline_config = pipeline_data["pipeline"]
        output_directory = pipeline_data.get("output_directory", "./output")

        # Process the pipeline
        json_to_pipeline(pipeline_config)

        # Store the pipeline information (simplified for example)
        pipelines[pipeline_id] = {
            "status": "created",
            "output_directory": output_directory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"pipeline_id": pipeline_id, "message": "Pipeline processing completed"}



@router.get("/pipeline/{pipeline_id}/status")
async def get_pipeline_status(pipeline_id: str):
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"pipeline_id": pipeline_id, "status": "Processing"}  # Example status

@router.get("/pipeline/{pipeline_id}/captions")
async def get_captions(pipeline_id: str):
    # Implement logic to fetch generated captions
    pass

@router.post("/pipeline/{pipeline_id}/captions")
async def submit_captions(pipeline_id: str, edited_captions: dict = Body(...)):
    # Implement logic to update the pipeline with edited captions
    pass

@router.get("/pipeline/{pipeline_id}/output")
async def get_output(pipeline_id: str):
    # Implement logic to fetch the output video
    pass
