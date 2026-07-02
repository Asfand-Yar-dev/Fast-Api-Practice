from typing import Annotated,List,Dict,Optional
from pydantic import BaseModel,computed_field,Field,EmailStr

class Students(BaseModel):
    id:Annotated[str,Field(description="The unique identifier for the student")]
    name:str
    age:Annotated[int,Field(description="The age of the student",gt=10,lt=100)]
    email:Optional[EmailStr] = None
    course:List[str]
    marks:Dict[str,int] = Field(..., description="A dictionary containing subject names as keys and marks as values",examples=[{
    "Math": 85,
    "Science": 90,
    "English": 88
    }])
    
    @computed_field
    @property
    def total_marks(self) -> int:
        return (sum(self.marks.values()))
    
    @computed_field
    @property
    def grade(self) -> str:
        total=self.total_marks
        if total >= 90:
            return "A"
        elif total >= 80:
            return "B"
        elif total >= 70:
            return "C"
        elif total >= 60:
            return "D"
        else:
            return "F"

class UpdateStudent(BaseModel):
    name:Optional[str] = None
    age:Optional[Annotated[int,Field(description="The age of the student",gt=10,lt=100)]] = None
    email:Optional[EmailStr] = None
    course:Optional[List[str]] = None
    marks:Optional[Dict[str,int]] = Field(None, description="A dictionary containing subject names as keys and marks as values",examples=[{
    "Math": 85,
    "Science": 90,
    "English": 88
    }])