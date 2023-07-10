from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session, joinedload
import traceback
from typing import List

router = APIRouter()
@router.post('/addprofessional', response_model=schema.professionalOut, status_code=status.HTTP_201_CREATED, tags=['Professional'])
async def addProfessional(professional : schema.professional, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        try:
            new_professional = models.Professional(**professional.dict(), user_id = current_user.user_id)
            db.add(new_professional)            
            db.commit()
            db.refresh(new_professional)
            return new_professional
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# get professional
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@router.get('/professional', response_model=schema.professionalOut, status_code=status.HTTP_200_OK, tags=['Professional'])
async def getProfessional(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # print("this is current user: ",current_user)
    # print("This is the current user ID:", current_user.user_id)
    professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()
    if not professional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professional with ID {id} does not exist")
    return professional
    # # Fetch user image data
    # user_image = db.query(models.UserImage).filter(models.UserImage.user_id == professional.user.user_id).first()
    # # print("user Image : ",user_image.image_id)
    # # Fetch qualifications data
    # qualifications = db.query(models.Qualification).filter(models.Qualification.professional_id == professional.professional_id).all()
    # # Fetch experiences data
    # experiences = db.query(models.Experience).filter(models.Experience.professional_id == professional.professional_id).all()
    
    # # Fetch reviews data
    # reviews = db.query(models.Reviews).filter(models.Reviews.professional_id == professional.professional_id).all()
    
    # # Create instances of the corresponding Pydantic models
    # user_image_data = None if not user_image else schema.userImageOut(**user_image.__dict__)

    # qualifications_data = [schema.qualificationInfo(**qualification.__dict__) for qualification in qualifications]
    # experiences_data = [schema.experienceInfo(**experience.__dict__) for experience in experiences]
    # reviews_data = [schema.ReviewsOut(**review.__dict__) for review in reviews]
    
    # # Create the response data using the professionalOut schema
    # professional_data = schema.professionalInfo(**professional.__dict__)
    # professional_out_data = schema.professionalOut(
    #     **professional_data.__dict__,
    #     user=schema.userOut(**professional.user.__dict__, userImage=user_image_data),
    #     qualification=qualifications_data,
    #     experience=experiences_data,
    #     reviews=reviews_data
    # )
    
    return professional_out_data


# delete post
@router.delete('/deleteprofessional', response_model= schema.professionalOut, status_code=status.HTTP_200_OK, tags=['Professional'])
async def deletePost(del_professional : schema.deletePost, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
            professional = db.query(models.Professional).filter(models.Professional.professional_id == del_professional.id)

            delete_professional = professional.first()
            if delete_professional == None:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"Post with Id : {del_professional.id} dose not exist")

        
            if delete_professional.user.user_id != current_user.user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
            
            deleted_qualifications = db.query(models.Qualification).filter(models.Qualification.professional_id == delete_professional.professional_id).delete()
            deleted_experiences = db.query(models.Experience).filter(models.Experience.professional_id == delete_professional.professional_id).delete()
            deleted_reviews = db.query(models.Reviews).filter(models.Reviews.professional_id == delete_professional.professional_id).delete()
            deleted_applications = db.query(models.Application).filter(models.Application.professional_id == delete_professional.professional_id).delete()
            deleted_following = db.query(models.Follow).filter(models.Follow.professional_id == delete_professional.professional_id).delete()
            
            professional.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 


@router.put('/updateprofessional/{id}', response_model= schema.professionalOut, status_code=status.HTTP_200_OK, tags=['Professional'])
async def updateProfessional(id : int, professional : schema.professional, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
            find_professional = db.query(models.Professional).filter(models.Professional.professional_id == id)
            update_professional = find_professional.first()

            if update_professional is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Professional with id {id}  does not exist")

            if update_professional.user.user_id != current_user.user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

            updated_professional = professional.dict()
            updated_professional.update({"user_id": current_user.user_id})

            find_professional.update(updated_professional, synchronize_session=False)
            db.commit()

            return update_professional
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# ##########################################
@router.get('/allprofessionals/', response_model=List[schema.professionalOut], status_code=status.HTTP_200_OK, tags=['Professional'])
async def getAllProfessional(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    professionals = db.query(models.Professional).all()

    if not professionals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Database is empty")
    return professionals
    # professional_out_list = []
    # for professional in professionals:
    #     user_image = db.query(models.UserImage).filter(models.UserImage.user_id == professional.user.user_id).first()

    #     # Fetch qualifications data
    #     qualifications = db.query(models.Qualification).filter(models.Qualification.professional_id == professional.professional_id).all()

    #     # Fetch experiences data
    #     experiences = db.query(models.Experience).filter(models.Experience.professional_id == professional.professional_id).all()

    #     # Fetch reviews data
    #     reviews = db.query(models.Reviews).filter(models.Reviews.professional_id == professional.professional_id).all()

    #     # Create instances of the corresponding Pydantic models
    #     user_image_data = None if not user_image else schema.userImageOut(**user_image.__dict__)

    #     qualifications_data = [schema.qualificationInfo(**qualification.__dict__) for qualification in qualifications]
    #     experiences_data = [schema.experienceInfo(**experience.__dict__) for experience in experiences]
    #     reviews_data = [schema.ReviewsOut(**review.__dict__) for review in reviews]

    #     # Create the response data using the professionalOut schema
    #     professional_data = schema.professionalInfo(**professional.__dict__)
    #     professional_out_data = schema.professionalOut(
    #         **professional_data.__dict__,
    #         user=schema.userOut(**professional.user.__dict__, userImage=user_image_data),
    #         qualification=qualifications_data,
    #         experience=experiences_data,
    #         reviews=reviews_data
    #     )
    #     professional_out_list.append(professional_out_data)

    # return professional_out_list

    # except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))

# ######################################## searching api ##########################################
@router.get('/search', response_model= List[schema.professionalOut], status_code=status.HTTP_200_OK, tags=['Professional'])
async def searchProfessional(keyword : schema.searchAPI, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # try:
        professionals = db.query(models.Professional).options(
            joinedload(models.Professional.qualifications),
            joinedload(models.Professional.experience)).filter(models.Professional.name.ilike(f"%{keyword.keyword}%")).all()
        print(professionals)
        
        if professionals is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
        
        professional_out_list = []
        for professional in professionals:
            professional_out = schema.professionalOut(
                professional_id=professional.professional_id,
                gender=professional.gender,
                intern_status=professional.intern_status,
                current_position=professional.current_position,
                address=professional.address,
                part_time=professional.part_time,
                registeration_no = professional.registeration_no,
                user=schema.userOut(
                    user_id=professional.user.user_id,
                    name = professional.user.name,
                    email = professional.user.email,
                    user_type = professional.user.user_type
                    ),
                qualification=[
                    schema.qualificationInfo(
                        qualification_id=qualification.qualification_id,
                        qualification = qualification.qualification,
                        # degree=qualification.degree,
                        # college=qualification.college,
                        # grade=qualification.grade,
                        # start_date=qualification.start_date,
                        # completion_date=qualification.completion_date,
                    ) for qualification in professional.qualifications
                ],
                experience=[
                    schema.experienceInfo(
                        experience_id=experience.experience_id,
                        experience = experience.experience
                        # company=experience.company,
                        # role=experience.role,
                        # description=experience.description,
                        # start_date=experience.start_date,
                        # end_date=experience.end_date,
                    ) for experience in professional.experience
                ],
            )
            professional_out_list.append(professional_out)

        return professional_out_list
        
    # except Exception as e:
        # raise HTTPException(status_code=500, detail=str(e))
