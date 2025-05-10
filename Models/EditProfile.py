from pydantic import BaseModel
from typing import Optional

class EditProfileSchema(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "phone_number": "+94771234567",
                "address": "123, Colombo, Sri Lanka"
            }
        }
