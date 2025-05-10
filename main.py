import uvicorn
from fastapi import FastAPI, Depends, Request, Security
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import SignInSchema, SignUpSchema
from Models.SetRoleSchema import SetRoleSchema
from Models.EditProfileSchema import EditProfileSchema 
import pyrebase

# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, auth

# Initialize FastAPI app
app = FastAPI(
    title="User Account Management Service",
    version="1.0.0",
    docs_url="/",
    description="Microservice for managing user accounts",
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True},
    openapi_tags=[{"name": "User", "description": "Operations related to user management"}]
)

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("ecommerce-microservices.json")
    firebase_admin.initialize_app(cred)

# Firebase Configuration for pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyCBfjkzq1bVn1boykZnigtiBnRKmrAxXsI",
    "authDomain": "ctse-b9a86.firebaseapp.com",
    "projectId": "ctse-b9a86",
    "storageBucket": "ctse-b9a86.firebasestorage.app",
    "messagingSenderId": "615106106940",
    "appId": "1:615106106940:web:0d0a035b5a75700f579539",
    "measurementId": "G-3QEHQMZJQG",
    "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebaseConfig)

# Security scheme for Swagger
security = HTTPBearer()


@app.get("/health", tags=["User"])
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}


@app.post("/SignUp", tags=["User"])
async def create_an_account(user: SignUpSchema):
    try:
        new_user = auth.create_user(email=user.email, password=user.password)
        return JSONResponse(status_code=201, content={"message": "User created successfully", "user_id": new_user.uid})
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail={"Email already exists": user.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/SignIn", tags=["User"])
async def sign_in(SignIn: SignInSchema):
    try:
        user = firebase.auth().sign_in_with_email_and_password(email=SignIn.email, password=SignIn.password)
        token = user['idToken']
        return JSONResponse(status_code=200, content={"message": "User signed in successfully", "token": token})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/validate_token", tags=["User"])
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    jwt = credentials.credentials
    try:
        user = auth.verify_id_token(jwt)
        return JSONResponse(status_code=200, content={
            "message": "Token is valid",
            "user_id": user['uid'],
            "role": user.get("role", "No role assigned")
        })
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/set_role", tags=["User"])
async def set_role(payload: SetRoleSchema):
    try:
        auth.set_custom_user_claims(payload.uid, {"role": payload.role})
        return JSONResponse(status_code=200, content={"message": f"Role '{payload.role}' has been set for user {payload.uid}"})
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.put("/edit_profile", tags=["User"])
async def edit_profile(
    payload: EditProfileSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        user_info = auth.verify_id_token(token)
        uid = user_info['uid']

        update_data = {}
        if payload.full_name:
            update_data['display_name'] = payload.full_name
        if payload.phone_number:
            update_data['phone_number'] = payload.phone_number

        if update_data:
            auth.update_user(uid, **update_data)

        return JSONResponse(status_code=200, content={"message": "Profile updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/view_profile", tags=["User"])
async def view_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_info = auth.verify_id_token(token)
        uid = user_info['uid']

        # Fetch user record from Firebase
        user_record = auth.get_user(uid)

        # Structure the response with useful details
        profile_data = {
            "uid": user_record.uid,
            "email": user_record.email,
            "full_name": user_record.display_name,
            "phone_number": user_record.phone_number,
            "email_verified": user_record.email_verified,
            "role": user_info.get("role", "No role assigned")
        }

        return JSONResponse(status_code=200, content={"message": "Profile fetched successfully", "profile": profile_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
