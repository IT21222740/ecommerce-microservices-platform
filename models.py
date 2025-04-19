from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email: str
    password: str


    class Config:
        schema_extra ={
            "example":{
                "email":"sample@gmail.com",
                "password":"samplepass123"
            }
        }



class SignInSchema(BaseModel):
    email: str
    password: str

    
    class Config:
        schema_extra ={
            "example":{
                "email":"sample@gmail.com",
                "password":"samplepass123"
            }
        }