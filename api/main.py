from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from .routes import pipeline  # Assuming this is your router import

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the pipeline router
app.include_router(pipeline.router)
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8000)))
