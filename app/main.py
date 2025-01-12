# app/api/main.py
import os
from fastapi import FastAPI
from app.api.v1.endpoints import drilling_companies, users, operators
from app.dependencies.database import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="DBradons Awesome API",
    description="API for managing drilling companies, users, and operators.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Drilling Companies",
            "description": "Operations related to drilling companies.",
        },
        {
            "name": "Users",
            "description": "Operations related to user management.",
        },
        {
            "name": "Operators",
            "description": "Operations related to operators.",
        },
    ],
)

# Include routers
app.include_router(drilling_companies.router, prefix="/drilling_companies", tags=["Drilling Companies"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(operators.router, prefix="/operators", tags=["Operators"])