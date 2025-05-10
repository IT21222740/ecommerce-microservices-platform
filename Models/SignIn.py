from pydantic import BaseModel

class SignInSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplepass123"
            }
        }