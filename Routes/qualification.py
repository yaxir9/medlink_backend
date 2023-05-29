from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List

router = APIRouter()

@router.post('/addQualification', response_model=schema.qualificationOut, status_code=status.HTTP_200_OK, tags=['Qualification'])
async def addQualification(qualification : schema.qualification, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        try:
            professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()
            new_qualification = models.Qualification(**qualification.dict(), professional_id = professional.professional_id)
            db.add(new_qualification)            
            db.commit()
            db.refresh(new_qualification)
            return new_qualification
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# allemployees
@router.get('/qualification/{id}', response_model=schema.qualificationOut, status_code=status.HTTP_200_OK, tags=['Qualification'])
async def getQualification(id : int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        # if current_user.user_type == 'organization':
        qualification = db.query(models.Qualification).filter(models.Qualification.qualification_id == id).first()
        return qualification
        # else:
        #  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


#response_model=schema.employeesOut,
@router.delete('/delete_qualification', status_code=status.HTTP_204_NO_CONTENT, tags=['Qualification'])
async def deleteQualification(delqualification: schema.employeesDelete, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':        
        qualification =  db.query(models.Qualification).filter(models.Qualification.qualification_id == delqualification.id)
        delete_qualification = qualification.first()
        if delete_qualification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with Id: {delEmployee.id} does not exist")

        if delete_qualification.professional.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
        print("ok")
        qualification.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# update employee data
@router.put('/update_qualification/{id}', response_model=schema.qualificationOut, status_code=status.HTTP_200_OK, tags=['Qualification'])
async def editQualification(id : int, qualification: schema.qualification, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':        

        find_qualification = db.query(models.Qualification).filter(models.Qualification.qualification_id == id)
        update_qualification = find_qualification.first()

        if update_qualification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {id} does not exist")

        if update_qualification.professional.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

        updated_qualification = qualification.dict()
        updated_qualification.update({"professional_id": update_qualification.professional_id})

        find_qualification.update(updated_qualification, synchronize_session=False)
        db.commit()

        return update_qualification
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")