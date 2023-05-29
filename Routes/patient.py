from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List

router = APIRouter()

@router.post('/addpatient', response_model=schema.PatientOut, status_code=status.HTTP_200_OK, tags=['Patient'])
async def addPatient(patient : schema.Patient, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        if current_user.user_type == 'patient':
            try:
                new_patient = models.Patient(**patient.dict(), user_id = current_user.user_id)
                db.add(new_patient)            
                db.commit()
                db.refresh(new_patient)
                return new_patient
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")
    

# allemployees
@router.get('/patient/{id}', response_model=schema.PatientOut, status_code=status.HTTP_200_OK, tags=['Patient'])
async def getPatient(id : int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
            try:
                patient = db.query(models.Patient).filter(models.Patient.patient_id == id).first()
                return patient

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@router.get('/allpatients', response_model=List[schema.PatientOut], status_code=status.HTTP_200_OK, tags=['Patient'])
async def allPatient( db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        patients = db.query(models.Patient).all()
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

