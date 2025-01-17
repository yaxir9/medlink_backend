from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import List, Optional
# user schema


class userImage(BaseModel):
    path : str 


class userImageOut(userImage):
    image_id : int 
    created_at : date
    user_id : int 
    class Config:
        orm_mode = True 


class User(BaseModel):
    name : str
    email : EmailStr
    user_type : str 

class UserCreate(User):
    password : str

class userOut(User):
    user_id : int 
    userImage : Optional[userImageOut] 
    class Config:
        orm_mode = True


class userOut_with_Token(userOut):
    access_token : str
    token_type : str
    class Config:
        orm_mode = True

    


class delteUser(BaseModel):
    id : int

class qualification(BaseModel):
    degree : str 
    college : str 
    grade : str 
    start_date : date
    completion_date : date
    qualification : str 

class qualificationInfo(qualification):
    qualification_id : int 
    class Config:
        orm_mode = True



class experience(BaseModel):
    company : str 
    role : str 
    description : str 
    start_date : date
    end_date : date
    experience : str 

class experienceInfo(experience):
    experience_id : int 
    class Config:
        orm_mode = True



class professional(BaseModel):
    gender: str 
    intern_status: bool 
    current_position: str 
    address: str 
    part_time: bool
    phone_no: Optional[str] = None
    registeration_no: Optional[str] = None

class professionalInfo(professional):
    professional_id : int 
    user: userOut

    class Config:
        orm_mode = True

class qualificationOut(qualificationInfo):
    professional : professionalInfo
    class Config:
        orm_mode = True

class experienceOut(experienceInfo):
    professional : professionalInfo
    class Config:
        orm_mode = True

class Reviews(BaseModel):
    rating: float
    professional_id : int 


class ReviewsOut(Reviews):
    reviews_id : int 
    patient_id : int 
    date : date 
    class Config:
        orm_mode = True 

class professionalOut(professionalInfo):
    qualification: List[qualificationInfo] = []
    experience: List[experienceInfo] = []
    reviews : List[ReviewsOut] = []
    class Config:
        orm_mode = True
    



class organization(BaseModel):
    org_type : str 
    phone_no : str 
    address : str 


class organizationInfo(organization):
    organization_id : int 
    user : userOut
    class Config:
        orm_mode = True


class employees(BaseModel):
    name : str 
    specialization : str 
    image_path : str = None
class employeesOut(employees): 
    employee_id : int 
    
    organization : organizationInfo
    class Config:
        orm_mode = True

class employeesDelete(BaseModel):
    id : int 
    

class post(BaseModel):
    job_type : str 
    description : str 
    salary  : int 
    deadline : date

class postsInOrg(post):
    post_id : int 
    date : date 
    class Config:
        orm_mode = True


class postOut(post):
    post_id : int 
    date : date 
    organization_id : int 
    organization : organizationInfo
    class Config:
        orm_mode = True

class deletePost(BaseModel):
    id : int 

class Follow(BaseModel):
    organization_id : int 

class FollowersOut(Follow):
     
    follow_id : int 
    professional_id : int 
    date : date 
    class Config:
        orm_mode=True 

class organizationOut(organizationInfo):

    employees : List[employeesOut] 
    posts : List[postsInOrg]
    follower: List[FollowersOut]
    class Config:
        orm_mode = True

class deleteOrganization(BaseModel):
    id : int 

    
class Token(BaseModel):
    access_token : str
    token_type : str
    
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : Optional[str] = None

class searchAPI(BaseModel):
    keyword : str 


class Application(BaseModel):
    application_id : int 
    post_id : int 
    professional_id : int 


class ApplicationOut(Application):
        date : date 
        professional : professionalOut
        class Config:
            orm_mode = True 



class Patient(BaseModel):
    # name : str 
    address : str 
    phone_no : str 

class PatientOut(Patient):
    patient_id : int 
    user : userOut 
    class Config:
        orm_mode = True 




