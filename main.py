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

# Firebase Configuration
firebaseConfig = {
  "apiKey": "AIzaSyCkeYLF7sUEHQdURFZm-bRvAs5jL7u5faE",
  "authDomain": "ecommerce-microservices-93118.firebaseapp.com",
  "projectId": "ecommerce-microservices-93118",
  "storageBucket": "ecommerce-microservices-93118.firebasestorage.app",
  "messagingSenderId": "778737608790",
  "appId": "1:778737608790:web:aec96b98f4d70b1453f3f7",
  "measurementId": "G-541YPPWKZE",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)