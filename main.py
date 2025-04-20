import uvicorn
from fastapi import FastAPI
from models import SignInSchema, SignUpSchema
import pyrebase
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
import os


app = FastAPI(
    description="Microservice for managing user accounts",
    title="User Account Management Service",
    docs_url="/",
    version="1.0.0",
)


# Firebase Initialization
firebase = None
auth = None

# ✅ Load Firebase only if not running tests
if os.getenv("TESTING", "false") != "true":
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth

    if not firebase_admin._apps:
        cred = credentials.Certificate("ecommerce-microservices.json")
        firebase_admin.initialize_app(cred)

    auth = firebase_auth
else:
    # In test mode, set `auth` to a mock object to avoid NoneType errors
    from unittest.mock import MagicMock
    auth = MagicMock()

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

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy"}

firebase = pyrebase.initialize_app(firebaseConfig)


@app.post("/SignUp")
async def create_an_account(user: SignUpSchema):
    email = user.email
    password = user.password
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        return JSONResponse(status_code=201, content={"message": "User created successfully", "user_id": user.uid})
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail={"Email already exists":user.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user")

@app.post("/SignIn")
async def sign_in(SignIn: SignInSchema):
    email= SignIn.email
    password= SignIn.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(email=email, password=password)
        token = user['idToken']
        return JSONResponse(status_code=200, content={"message": "User signed in successfully", "token": token})
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

@app.post("/validate_token")
async def validate_token(request:Request):
    headers = request.headers
    jwt = headers.get("Authorization")
    if jwt is None:
        raise HTTPException(status_code=401, detail="Token not provided")
    
    user = auth.verify_id_token(jwt)
    return JSONResponse(status_code=200, content={"message": "Token is valid", "user_id": user['uid']})
    

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)