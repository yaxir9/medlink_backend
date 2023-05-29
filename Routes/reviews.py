from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List

router = APIRouter()

@router.post('/addreviews', response_model=schema.ReviewsOut, status_code=status.HTTP_200_OK, tags=['Reviews'])
async def addReviews(reviews: schema.Reviews, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type == 'patient':
        try:
            patient = db.query(models.Patient).filter(models.Patient.user_id == current_user.user_id).first()

            new_reviews = models.Reviews( **reviews.dict(), patient_id=patient.patient_id)
            db.add(new_reviews)
            db.commit()
            db.refresh(new_reviews)
            return new_reviews
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")


@router.get('/getreviews/{id}', response_model=schema.ReviewsOut, status_code=status.HTTP_200_OK, tags=['Reviews'])
async def getReview(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    reviews = db.query(models.Reviews).filter(models.Reviews.reviews_id == id).first()
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reviews with ID {id} does not exist")
    return reviews

@router.get('/allreviews/', response_model=List[schema.ReviewsOut], status_code=status.HTTP_200_OK, tags=['Reviews'])
async def getAllReview(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    reviews = db.query(models.Reviews).all()
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reviews with ID {id} does not exist")
    return reviews
            
