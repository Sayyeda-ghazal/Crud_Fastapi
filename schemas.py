from pydantic import BaseModel , Field, validator, EmailStr

class Book(BaseModel):
    task : str = Field(description="Name of product", min_length=3, max_length=20)
    class Config:
        orm_mode = True

    @validator('task')
    def check_for_numbers(cls, value):
        if any(char.isdigit() for char in value):  
            raise ValueError("Task cannot contain any numbers")
        return value
    
class login(BaseModel):
    username: str
    email: EmailStr
    password: str

class createuserrequest(BaseModel):
    username:str
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str
