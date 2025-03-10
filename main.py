"""
    This API Script follows PEP 8 styling format of python. 
"""

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from validation import EmployeeInsertion, EmployeeUpdate


DATABASE_URL = "mysql+pymysql://root:@localhost:3306/spreadme"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create Table using SQLAlchemy ORM
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    designation = Column(String(255), nullable=False)
    salary = Column(Float, nullable=False)
Base.metadata.create_all(bind=engine)


def get_db():  # Get Database Session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees")  # Add new employees
def add_employee(employee: EmployeeInsertion, db: Session = Depends(get_db)):
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        designation=employee.designation,
        salary=employee.salary
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return {"message": "Employee added successfully", "employee": db_employee}


@app.get("/employees", response_model=List[dict])  # Fetch all employees
@app.get("/employees/{id}", response_model=dict)  # Fetch Employee by id
def fetch_employees(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        employee = db.query(Employee).filter(Employee.id == id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "designation": employee.designation,
            "salary": employee.salary
        }
    
    employees = db.query(Employee).all()
    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "designation": emp.designation,
            "salary": emp.salary
        }
        for emp in employees
    ]


@app.put("/employees/{id}")  # Edit Employee Details
def edit_details(id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == id).first()
    
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if employee_update.name:
        db_employee.name = employee_update.name
    if employee_update.email:
        db_employee.email = employee_update.email
    if employee_update.designation:
        db_employee.designation = employee_update.designation
    if employee_update.salary:
        db_employee.salary = employee_update.salary

    db.commit()
    db.refresh(db_employee)
    
    return {"message": "Employee details updated successfully", "employee": db_employee}


@app.delete("/employees/{id}")  # Delete an Employee
def delete_employees(id: int, db: Session = Depends(get_db)):
    if id:
        db_employee = db.query(Employee).filter(Employee.id == id).first()
        
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        db.delete(db_employee)
        db.commit()
        
        return {"message": "Employee deleted successfully", "employee_id": id}
