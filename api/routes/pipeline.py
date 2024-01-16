from fastapi import APIRouter, HTTPException, Body
import json
import uuid
from ..services.json_to_pipe import json_to_pipeline

router = APIRouter()

# Example in-memory storage for pipelines
pipelines = {}

@router.get("/")
async def read_root():
    return {"Hello": "World"}

# In routes/pipeline.py

@router.post("/pipeline")
async def create_pipeline(pipeline_data: dict = Body(...)):
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
