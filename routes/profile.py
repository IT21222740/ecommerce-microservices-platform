from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from Models import EditProfileSchema, SetRoleSchema

router = APIRouter()
security = HTTPBearer()

@router.post("/validate_token", tags=["User"])
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
    
@router.post("/set_role", tags=["User"])
async def set_role(payload: SetRoleSchema):
    try:
        auth.set_custom_user_claims(payload.uid, {"role": payload.role})
        return JSONResponse(status_code=200, content={"message": f"Role '{payload.role}' has been set for user {payload.uid}"})
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/edit_profile", tags=["User"])
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


@router.get("/view_profile", tags=["User"])
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
