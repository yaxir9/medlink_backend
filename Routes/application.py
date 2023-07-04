from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session, joinedload
import traceback
from typing import List
from fastapi import Query


router = APIRouter()
#
@router.post('/apply/{post_id}',   response_model=schema.ApplicationOut, status_code=status.HTTP_200_OK, tags=['Application'])
async def addApplication(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        # try:

            professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()
            print("professional id : ", professional.professional_id)
            post = db.query(models.Post).filter(professional.user_id == current_user.user_id).first()
            print("post id : ",post.post_id)
            print("Professional user : ", professional.user_id)
            print("current user : ",current_user.user_id)
            apply = {"post_id" : post_id, "professional_id" : professional.professional_id}
            new_apply = models.Application(**apply)
            db.add(new_apply)            
            db.commit()
            db.refresh(new_apply)
            return new_apply
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=str(e))

    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")


# get Applications
@router.get('/apply/{id}', response_model= schema.ApplicationOut, status_code=status.HTTP_200_OK, tags=['Application'])
async def getPost(id : int,  db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        if current_user.user_type.lower() == 'organization':
    
            apply = db.query(models.Application).filter(models.Application.application_id == id).first()

            if not apply:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"post at this {id} dose not exist")
            
            return apply
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 






# ########################################################

# @router.get('/applies/', response_model=List[schema.ApplicationOut], status_code=status.HTTP_200_OK, tags=['Application'])
# async def getAllApplications(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
#     if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
    
#         applications = db.query(models.Application).all()
#         if not applications:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Applications")

#         application_out_list = []
#         for application in applications:
#             professional = application.professional
#             qualifications = []
#             for qualification in professional.qualifications:
#                 qualification_out = schema.qualificationInfo(
#                     qualification_id=qualification.qualification_id,
#                     degree=qualification.degree,
#                     college=qualification.college,
#                     grade=qualification.grade,
#                     start_date=qualification.start_date,
#                     completion_date=qualification.completion_date
#                 )
#                 qualifications.append(qualification_out)

#             professional_out = schema.professionalOut(
#                 professional_id=professional.professional_id,
#                 name=professional.name,
#                 gender=professional.gender,
#                 intern_status=professional.intern_status,
#                 current_position=professional.current_position,
#                 address=professional.address,
#                 part_time=professional.part_time,
#                 registeration_no=professional.registeration_no,
#                 qualification=qualifications,
#                 experience=professional.experience,
#                 user=schema.userOut(
#                         user_id=professional.user.user_id,
#                         email = professional.user.email,
#                         user_type = professional.user.user_type
#                         )
#             )

#             application_out = schema.ApplicationOut(
#                 application_id = application.application_id,
#                 post_id = application.post_id,
#                 professional_id = application.professional_id,
#                 date=application.date,
#                 professional=professional_out
#             )
#             application_out_list.append(application_out)

#         return application_out_list

#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")  




@router.get('/applies/{post_id}', response_model=List[schema.ApplicationOut], status_code=status.HTTP_200_OK, tags=['Application'])
async def getAllApplications(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user)
):
    if current_user.user_type.lower() == 'organization':
        applications = db.query(models.Application).filter_by(post_id=post_id).all()
        if not applications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Applications")

        application_out_list = []
        for application in applications:
            professional = application.professional
            qualifications = []
            for qualification in professional.qualifications:
                qualification_out = schema.qualificationInfo(
                    qualification_id=qualification.qualification_id,
                    qualification=qualification.qualification,
                )
                qualifications.append(qualification_out)

            professional_out = schema.professionalOut(
                professional_id=professional.professional_id,
                gender=professional.gender,
                intern_status=professional.intern_status,
                current_position=professional.current_position,
                address=professional.address,
                part_time=professional.part_time,
                registeration_no=professional.registeration_no,
                qualification=qualifications,
                experience=professional.experience,
                user=schema.userOut(
                        user_id=professional.user.user_id,
                        name=professional.user.name,
                        email = professional.user.email,
                        user_type = professional.user.user_type
                        )
            )

            application_out = schema.ApplicationOut(
                application_id = application.application_id,
                post_id = application.post_id,
                professional_id = application.professional_id,
                date=application.date,
                professional=professional_out
            )
            application_out_list.append(application_out)

        return application_out_list

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")
