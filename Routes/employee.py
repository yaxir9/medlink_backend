from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends , UploadFile, File, Form
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List
from pathlib import Path
from fastapi.responses import FileResponse
import os 
router = APIRouter()

@router.post('/addemployee',  status_code=status.HTTP_200_OK, response_model=schema.employeesOut, tags=['Employees in Organization'])
async def addEmployee(name : str = Form(...),specialization: str = Form(...), image : UploadFile = File(...), db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    if current_user.user_type == 'organization':
        try:

            org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
            print(org.user_id)

            save_path = Path('static') / 'org_employees'
            save_path.mkdir(parents=True, exist_ok=True)
            file_path = save_path / f"{name}.{image.filename.split('.')[-1]}"
            with file_path.open('wb') as buffer:
                buffer.write(await image.read())

            employee = schema.employees(
                name=name,
                specialization=specialization,
                image_path= str(file_path),
                organization_id=org.organization_id  
            )
            new_employee = models.Employees(**employee.dict(),organization_id = org.organization_id)
            db.add(new_employee)            
            db.commit()
            db.refresh(new_employee)
            return new_employee
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))# all employees
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 

# allemployees
@router.get('/employee/{id}', response_model=schema.employeesOut, status_code=status.HTTP_200_OK, tags=['Employees in Organization'])
async def getEmployee(id : int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        if current_user.user_type == 'organization':
            try:
                employee = db.query(models.Employees).filter(models.Employees.employee_id == id).first()
                return employee

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 


@router.get("/employeeimage/{filename}", status_code=status.HTTP_200_OK, tags=['Employees in Organization'])
async def get_employee_image(filename: str, current_user : int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'organization':
        try:
            print("filename",filename)
            return FileResponse(filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))# all employees
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 



# org all employees
@router.get('/employees/', response_model= List[schema.employeesOut], status_code=status.HTTP_200_OK, tags=['Employees in Organization'])
async def orgPosts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'organization':
        org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()

        if org:
            employees = db.query(models.Employees).filter(models.Employees.organization_id == org.organization_id).all()
            if not employees:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"In this organization has no employees")
            return employees 
    else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 




@router.get('/allemployees', response_model=List[schema.employeesOut], status_code=status.HTTP_200_OK, tags=['Employees in Organization'])
async def allEmployees( db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'organization':
        try:
            employees = db.query(models.Employees).all()
            return employees
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 

#  response_model=schema.employeesOut,
@router.delete('/delete_employee', status_code=status.HTTP_204_NO_CONTENT, tags=['Employees in Organization'])
async def deleteEmployee(delEmployee: schema.employeesDelete, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'organization':

        employee = db.query(models.Employees).filter(models.Employees.employee_id == delEmployee.id)
        delete_employee = employee.first()
        
        if delete_employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with Id: {delEmployee.id} does not exist")

        if delete_employee.organization.user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

        file_path = delete_employee.image_path

        # Check if the file exists before deleting
        if os.path.exists(file_path):
            os.remove(file_path)


        employee.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")


# update employee data
@router.put('/updateemployee/{id}', response_model=schema.employeesOut, status_code=status.HTTP_200_OK, tags=['Employees in Organization'])
async def editEmployee(id : int, name : str = Form(...),specialization: str = Form(...), image : UploadFile = File(...),  db:  Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'organization':
        find_employee = db.query(models.Employees).filter(models.Employees.employee_id == id)
        update_employee = find_employee.first()

        if update_employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {id} does not exist")

        if update_employee.organization.user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

        org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
        print(org.user_id)

        save_path = Path('static') / 'org_employees'
        save_path.mkdir(parents=True, exist_ok=True)
        file_path = save_path / f"{name}.{image.filename.split('.')[-1]}"
        with file_path.open('wb') as buffer:
            buffer.write(await image.read())

        employee = schema.employees(
                name=name,
                specialization=specialization,
                image_path= str(file_path),
                organization_id=org.organization_id  
        )


        find_employee.update(employee.dict(), synchronize_session=False)
        db.commit()

        return update_employee
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

@router.delete('/delete_all_employees', status_code=status.HTTP_204_NO_CONTENT, tags=['Employees in Organization'])
async def deleteAll(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'organization':
        org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
        # Delete all employees with the same organization ID
        deleted_count = db.query(models.Employees).filter(models.Employees.organization_id == org.organization_id).delete()
        
        # Commit the changes to the database
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")