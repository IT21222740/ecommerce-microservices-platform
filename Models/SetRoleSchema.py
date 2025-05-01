from pydantic import BaseModel

class SetRoleSchema(BaseModel):
    uid: str
    role: str  # "admin"
    class Config:
        json_schema_extra ={
            "example":{
                "uid":"sampleuid123",
                "role":"admin"
            }
        }