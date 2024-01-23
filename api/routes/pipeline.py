from fastapi import FastAPI, Depends, APIRouter, HTTPException, Body, File, UploadFile
import json
from fastapi.security import OAuth2PasswordBearer
import uuid
import time
import jwt
print(jwt.__file__)
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
        token = token[7:].strip('"')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # Add additional validation here if necessary (e.g., check 'sub' field in payload)
        except Exception as e:
            print(f"h3 - Exception: {str(e)}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid token")

        return await func(*args, **kwargs)
    return wrapper


router = APIRouter()

# Example in-memory storage for pipelines
pipelines = {}
file_paths = {}

@router.get("/")
async def read_root():
    return {"Hello": "World"}

# In routes/pipeline.py

@router.post("/pipeline")
@token_validator
async def create_pipeline(request: Request, pipeline_data: dict = Body(...), file_path: str = ""):
    pipeline_id = str(uuid.uuid4())
    pipeline_data = pipeline_data["body"]
    try:
        # Extract the pipeline configuration and output directory
        pipeline_config = pipeline_data["pipeline"]
        print(pipeline_config)
        output_directory = pipeline_data.get("output_directory", "./output")
        print(output_directory)
        if pipeline_config["directory"] == '' and file_paths["balls"] != "":
            print("here")
            pipeline_config["directory"] = file_paths.get("balls", "")

        # Process the pipeline
        json_to_pipeline(pipeline_config)

        # Store the pipeline information (simplified for example)
        pipelines[pipeline_id] = {
            "status": "created",
            "output_directory": output_directory
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"pipeline_id": pipeline_id, "message": "Pipeline processing completed"}

@router.post("/upload")
@token_validator
async def upload_file(request: Request, file: UploadFile = File(...)):
    # Save the file to a directory
    with open(f"example_videos/input_vids/{file.filename}", "wb") as buffer:
        # Read the file in chunks and save it
        for data in iter(lambda: file.file.read(10000), b""):
            buffer.write(data)

    unique_key = "balls"  # Generate or retrieve a unique key
    file_paths[unique_key] = "example_videos/input_vids/"
    print(file_paths)
    return {"filename": file.filename}


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
