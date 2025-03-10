from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class EmployeeInsertion(BaseModel):  # Validation for Employee Creation
    id: Optional[int] = Field(None, description="Primary Key, Auto-increment")
    name: str
    email: EmailStr
    designation: str
    salary: float


class EmployeeUpdate(BaseModel):  # Validation for Employee Update
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    designation: Optional[str] = None
    salary: Optional[float] = None
