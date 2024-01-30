from fastapi import FastAPI, Depends, APIRouter, HTTPException, Body, File, UploadFile
import json
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
import uuid
import time, os
import jwt
from functools import wraps
from typing import Optional
from ..services.auth.auth import token_validator
from ..services.preprocessing.preprocessing import parse_pipeline_data, json_to_pipeline
from ..services.processing.execute import execute_pipeline

from fastapi import HTTPException, Request, status
from functools import wraps

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
    
    input_directory = ""
    # try:
    if user_id in file_paths and file_paths[user_id] != "":
        input_directory = file_paths[user_id]
    else:
        input_directory = f"example_videos/input_vids/{user_id}"
    # except:
    #     raise HTTPException(status_code=400, detail="User input folder not found")
    
    output_directory = f"output/{user_id}"
    os.makedirs(output_directory, exist_ok=True)
    # os.remove(output_directory)

    pipeline_id = str(uuid.uuid4())
    try:
        pipeline = json_to_pipeline(pipeline_data["body"])
        execute_pipeline(input_directory, output_directory, pipeline)
        pipelines[pipeline_id] = {
            "status": "created",
            "output_directory": output_directory
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return {"pipeline_id": pipeline_id, "message": "Pipeline Created"}


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
def get_pipeline_status(pipeline_id: str):
    pipeline_get = execute_pipeline(pipeline_id)
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"pipeline_id": pipeline_id, "status": pipelines[pipeline_get]}  # Example status


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