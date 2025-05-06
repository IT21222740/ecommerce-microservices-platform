import uvicorn
from fastapi import FastAPI, Depends, Request, Security
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import SignInSchema, SignUpSchema
from Models.SetRoleSchema import SetRoleSchema
from Models.EditProfileSchema import EditProfileSchema
import pyrebase
import json
import base64


#encoding = "utf-8"
encoded_json = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiY3RzZS1iOWE4NiIsCiAgInByaXZhdGVfa2V5X2lkIjogImZmODQyNDU1OGU5ZjQ4NjA2MzdiYThlNjc1NTU2ZGIwYmVhNTAyNjMiLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2Z0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktnd2dnU2tBZ0VBQW9JQkFRRG9yNHFqVWdMMEh6YnVcbkVURXNMd0NObmJKR3hhNHo2cExtNEFReG4yTDNFemEyekVmWXptTmdiYUU5dTBnS1N4MWdoM21QNVdleUY4QU1cbnh3N2ZienQ1SEpOSjdwZUt1d2l5b2Q1ZUxyT2RWNFZnKzFkZVZxaXZyUThLTWJIVTQ2NTFjeTJkaGZmNlNPcGRcbnVaZ1VieCtIYWxmVGtoVHFoKzlMUWNxdjdHQmF5MkhheHRzTHkxeWhVRHJVb2ZCVzFMUnJxYnRoS2dhYy9YenVcbmhLd29HbE5tck1lcWk4UDk3bGtuQTRJY2NZL2VUL1dpVE05U3EyRXh3Sm83QWRWSzR1RHdmSTZja3hLSkp5cmtcbjFsOTRIYnRXWTVMTzVXeEtTY3ZmRlE5cWxhS1FjbTFsd0RkYUQzcVBWbFRrMVk4ZXpPbDFVYW1HTmxZKzlzK3NcbjB6VHl2ei9aQWdNQkFBRUNnZ0VBVFlBK2dKUnQyR3JYTEdjOGhoZG5xME9Wb0IzeW5tY29vODZFaHhTcjdWaVFcbmRrVkhQdTdMU2RCcURyb2t6Z3pqellXQ0Ywd1ZCRXdGMHh1d0YvcWdDQUJkREpoMEVDaW94bnJFcW9FS29VTUhcbjhWdjE1ejJjOU5xQzhtWEg4ZjBkM0EvUFp6SzZmRG95R2FLYUJXQlgwNDQzajRnT0FHbmphYUVSeGhQSXFpU0dcbkROWU9GM2FUa0t4ekptOEpMck84VG03b3dJY0hPd00xMjBMYXpybStzdVRDMEdjNEEzNjBmbFN0Smh6Uktnb2dcbnBDSGt5WUZqSm00VS9lL2c3U0tEblpvcDRRYi9xdmd5K3dhc2I4enNUbDRLdHZUTXByQmh3bzlLMmdxRnBWNXBcbmNoVEJuVXFZSk50ZFlYOEVDQmVnOW5vbUJIOG9wdDZMbVMvR2dHOXFnd0tCZ1FEK0w2ZVB4UnViYnQzTjNDNU9cbk4xSzU4YS9YVGIrUnhOaWEzYmM4R09MOGZDTUUrWDNMR0pPZkhGZ1JzTGgraWwrL0xpemZQempocWV5NVVPdGZcblpGdlNoc25GRVhiSDhQK3Z1dzRHcWVtaTgrdVdJR1JwTkxUODZSVmo1SVJoejBiUlRJb0h3dDBveCtkeHhzNC9cbm5GN1hkbnlkeWNpdGl0WnJwN051YnhrYU13S0JnUURxV0p3em9mZkIwTkdmUnptZFZGa2w1WWoyUGpDTnBlb21cbjMzWVNIbkd2cHlDVlVoeWxDaXZWVTNISkc5bnAraHNkMy84YzE1U3FUZEE4N2k2b0ZXTDZpMjRhalFTSTBvWmxcbkNUMzNIb0xibWh0ckxNNWlobkY1Skw2Nyt0QXBXbUdvMFQzaUJjQ0FoVXpRcnM4dVdwQzVxcGNZQitzRmZOaGtcbjZoclMrUG1Kd3dLQmdRRENheEsvN2FSN0U2YUZnYWJOWHBWZzhoSnNIT1N0Q3lJZCtmM2Y4cTBUTDZQZGR6TVhcbk45b1p0aVZLaXAvaThkWGdOZUpPYzEzL2hPZ3lxa2tOc29abEZZR1l3UTNZU21aWE5EeTdMaFVzOVdLNWRsYzJcbi9RQjkvWTNGMVJESWV6RVFmM21JREN6NnQwUTRpelpRQXp1cms4NG5KaUxmVWpWRkxJVWFyOUZFYndLQmdRQ0VcbndoUWpjQU5TaWtEbXNjdmk1RERvdGlNa0ZORWV2YnByc1RaTFIzSHlKNFRlOHJpRmlzQ1FSb2gwZk5HenFsdUlcblRpaFJKNVB4OHNrZ2EzS0ZDRENkYlRXLzF0bVZ4V1liZ09QWXhqRXR4Uno1VjFYSUhRL1ZxRXBoWmRKZFN2VitcblZLTnhFdjhlRCtZWFpxQzZTdFlvU0lyMk15NGlXcnFnV0xzL2Y0cW1Ud0tCZ0VFa2VMTTR4V0V2eDlkSEczc2Rcbk9oVndMUVppRENtbWZrbUJYY3dsNzBRRDVoOTFoWmsvV2ZYOUxodmMzWTVMTDV5YURPaHhJQmQyRDRsb1lYcTJcblZnei83bE1GclFMN0JBWDJIdzc5SXRMbUJXTzcyaEp2VlVBK2NlNWsvWUVWTDVKUUI2UmJyRmlQNE1pSDc3RkhcbnBLVGptajdsMWVISlpYSmlEQzg3YWNHUlxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogImZpcmViYXNlLWFkbWluc2RrLWZic3ZjQGN0c2UtYjlhODYuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJjbGllbnRfaWQiOiAiMTA0ODA0NTg4MDY2MzgzNDU3NjUyIiwKICAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLAogICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLAogICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwKICAiY2xpZW50X3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vcm9ib3QvdjEvbWV0YWRhdGEveDUwOS9maXJlYmFzZS1hZG1pbnNkay1mYnN2YyU0MGN0c2UtYjlhODYuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20iCn0K"

# Decode the base64
decoded_bytes = base64.b64decode(encoded_json)
service_account_data = json.loads(decoded_bytes.decode("utf-8"))


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
    cred = credentials.Certificate(service_account_data)
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
