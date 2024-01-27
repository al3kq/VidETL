from fastapi import FastAPI, Depends, APIRouter, HTTPException, Body, File, UploadFile
import json
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
import uuid
import time, os
import jwt
from functools import wraps
from typing import Optional
from ..services.json_to_pipe import json_to_pipeline


class uiInput:
    def __init__(self, id, input_video_path, status, data) -> None:
        self.id
        self.input_video_path
        self.status
        self.data
    


from fastapi import HTTPException, Request, status
from functools import wraps

SECRET_KEY = "DEVJWTSECRET"  # Replace with your actual key

ALGORITHM = "HS256"

# def token_validator(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         request = kwargs.get('request')
#         if request is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="Request object not found")

#         token = request.headers.get("Authorization")
#         if not token or not token.startswith("Bearer "):
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="Token not found or invalid")
#         token = token[7:].strip('"')
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#             # Add additional validation here if necessary (e.g., check 'sub' field in payload)
#         except Exception as e:
#             print(f"h3 - Exception: {str(e)}")
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="Invalid token")
#         kwargs['payload'] = payload
#         return await func(*args, **kwargs)
#     print(wrapper)
#     return wrapper

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

router = APIRouter()

# Example in-memory storage for pipelines
pipelines = {}
file_paths = {}

@router.get("/")
async def read_root():
    return {"Hello": "World"}

# In routes/pipeline.py

@router.post("/pipeline")
async def create_pipeline(request: Request, pipeline_data: dict = Body(...), payload: dict = Depends(token_validator)):
    if payload is None:
        raise HTTPException(status_code=400, detail="Payload not found")
    
    user_id = payload.get("id")  # Assuming 'user_id' is a field in your payload
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID not found in payload")
    
    pipeline_id = str(uuid.uuid4())
    pipeline_data = pipeline_data["body"]
    try:
        print(pipeline_data)
        print(file_paths)
        # Extract the pipeline configuration and output directory
        pipeline_config = pipeline_data["pipeline"]
        output_directory = pipeline_data.get("output_directory", "./output")
        if pipeline_config["directory"] == '' and file_paths[user_id] != "":
            pipeline_config["directory"] = file_paths.get(user_id, "")

        print(pipeline_config["directory"])

        # Process the pipeline
        json_to_pipeline(pipeline_config)
        print("here")

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
async def upload_file(request: Request, file: UploadFile = File(...), payload: dict = Depends(token_validator)):
    if payload is None:
        raise HTTPException(status_code=400, detail="Payload not found")
    
    user_id = payload.get("id")  # Assuming 'user_id' is a field in your payload
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID not found in payload")
    
    user_dir = f"example_videos/input_vids/{user_id}"
    os.makedirs(user_dir, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    file_path = os.path.join(user_dir, unique_filename)
    # Save the file to a directory
    with open(file_path, "wb") as buffer:
        # Read the file in chunks and save it
        for data in iter(lambda: file.file.read(10000), b""):
            buffer.write(data)

    unique_key = user_id  # Generate or retrieve a unique key
    file_paths[unique_key] = user_dir
    print(file_paths)
    return {"filename": file.filename}


@router.get("/download")
async def download_file():
    file_path = "output/test_output_filename.mp4"  # Path to your MP4 file

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path, 
        media_type='video/mp4', 
        filename="downloaded_file.mp4",
        headers={"Content-Disposition": "attachment; filename=downloaded_file.mp4"}
    )


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