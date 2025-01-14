from pydantic import BaseModel , Field, validator

class Book(BaseModel):
    task : str = Field(description="Name of product", min_length=3, max_length=20)
    class Config:
        orm_mode = True

    @validator('task')
    def check_for_numbers(cls, value):
        if any(char.isdigit() for char in value):  # Check if any character is a number
            raise ValueError("Task cannot contain any numbers")
        return value