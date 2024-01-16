from fastapi import FastAPI
from .routes import pipeline

app = FastAPI()

# Include the pipeline router
app.include_router(pipeline.router)