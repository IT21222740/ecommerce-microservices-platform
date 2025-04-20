import uvicorn
from fastapi import FastAPI
from models import SignInSchema, SignUpSchema
import pyrebase


app = FastAPI(
    description="Microservice for managing user accounts",
    title="User Account Management Service",
    docs_url="/",
    version="1.0.0",
)


# Firebase Initialization
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate("ecommerce-microservices.json")
    firebase_admin.initialize_app(cred)

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)