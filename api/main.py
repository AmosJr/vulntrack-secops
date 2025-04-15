# Main entry point for the FastAPI application
from fastapi import FastAPI
from api import routes

# Create the FastAPI app with metadata
app = FastAPI(
    title="VulnTrack API",                                 # API title shown in Swagger
    description="API to query and manage security vulnerabilities",  # API description
    version="1.0.0"                                         # Version
)

# Include all the routes defined in routes.py
app.include_router(routes.router)
