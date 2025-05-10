from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from firebase_admin import auth
from utils.firebase import firebase
from Models import SignUpSchema, SignInSchema

router = APIRouter()


@router.post("/SignUp", tags=["User"])
async def create_an_account(user: SignUpSchema):
    try:
        new_user = auth.create_user(email=user.email, password=user.password)
        return JSONResponse(status_code=201, content={"message": "User created successfully", "user_id": new_user.uid})
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail={"Email already exists": user.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/SignIn", tags=["User"])
async def sign_in(SignIn: SignInSchema):
    try:
        user = firebase.auth().sign_in_with_email_and_password(email=SignIn.email, password=SignIn.password)
        token = user['idToken']
        return JSONResponse(status_code=200, content={"message": "User signed in successfully", "token": token})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
