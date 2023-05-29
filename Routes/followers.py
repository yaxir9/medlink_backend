from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List

router = APIRouter()


@router.post('/follow', response_model=schema.FollowersOut, status_code=status.HTTP_201_CREATED, tags=['Follow'])
# 
async def Follow(follower : schema.Follow, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        try:
            professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()
    
            new_follower = models.Follow(**follower.dict(), professional_id = professional.professional_id )
            db.add(new_follower)
            db.commit()
            db.refresh(new_follower)
            return new_follower

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# get follower
@router.get('/follower/{id}', response_model=schema.FollowersOut, status_code=status.HTTP_200_OK, tags=['Follow'])
async def get_follower(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        follower = db.query(models.Follow).filter(models.Follow.follow_id == id).first()
        if follower is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follower not found")
        return follower



@router.get('/orgfollowers', response_model=List[schema.FollowersOut], status_code=status.HTTP_200_OK, tags=['Follow'])
async def allFollowers( db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    
    org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    followers = db.query(models.Follow).filter(models.Follow.organization_id == org.organization_id).all()
    if followers is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="0 Followers")
    return followers


@router.get('/following', response_model=List[schema.FollowersOut], status_code=status.HTTP_200_OK, tags=['Follow'])
async def allFollowers( db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()

    following = db.query(models.Follow).filter(models.Follow.professional_id == professional.professional_id).all()
    if following is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following someone")
    return following



@router.get('/allfollowers', response_model=List[schema.FollowersOut], status_code=status.HTTP_200_OK, tags=['Follow'])
async def allFollowers( db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        followers = db.query(models.Follow).all()
        return followers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/unfollow', status_code=status.HTTP_204_NO_CONTENT, tags=['Follow'])
async def UnFollow(unfollow: schema.employeesDelete, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        # porfessional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()
        # if not professional:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following this organization")

        follower = db.query(models.Follow).filter(models.Follow.follow_id == unfollow.id)
        unfollow = follower.first()
        if unfollow is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found follower with this id")

        if unfollow.professional.user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
        follower.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")