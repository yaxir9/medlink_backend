from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List

router = APIRouter()

# add Experience
@router.post('/addExperience', response_model=schema.experienceOut, status_code=status.HTTP_200_OK, tags=['Experience'])
async def addExperience(experience : schema.experience, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        try:
            professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()
            new_experience = models.Experience(**experience.dict(), professional_id = professional.professional_id)
            db.add(new_experience)            
            db.commit()
            db.refresh(new_experience)
            return new_experience
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# allemployees
@router.get('/experience/{id}', response_model=schema.experienceOut, status_code=status.HTTP_200_OK, tags=['Experience'])
async def getExperience(id : int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        # if current_user.user_type == 'organization':
        experience = db.query(models.Experience).filter(models.Experience.experience_id == id).first()
        return experience
        # else:
        #  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


#response_model=schema.employeesOut,
@router.delete('/delete_exeprience', status_code=status.HTTP_204_NO_CONTENT, tags=['Experience'])
async def deleteExperience(delexperience: schema.employeesDelete, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':        
        experience =  db.query(models.Experience).filter(models.Experience.experience_id == delexperience.id)
        delete_experience = experience.first()
        if delete_experience is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Experience with Id: {delexperience.id} does not exist")

        if delete_experience.professional.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
        print("ok")
        experience.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# update employee data
@router.put('/update_experience/{id}', response_model=schema.experienceOut, status_code=status.HTTP_200_OK, tags=['Experience'])
async def editExperience(id: int, experience: schema.experience, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':        

        find_experience = db.query(models.Experience).filter(models.Experience.experience_id == id)
        update_experience = find_experience.first()

        if update_experience is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with ID {id} does not exist")

        if update_experience.professional.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

        updated_experience = experience.dict()
        updated_experience.update({"professional_id": update_experience.professional_id})

        find_experience.update(updated_experience, synchronize_session=False)
        db.commit()

        return update_experience
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")