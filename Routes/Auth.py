from fastapi import  APIRouter ,status, HTTPException , Depends, Response,Header, Request
from fastapi.security import OAuth2PasswordRequestForm
# from .. import models, schema, utils
import models, utils, Oauth2 
from db import  get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

@router.post('/Login', tags=['Login'])
async def Login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    
        user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
        
        if not user:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail='User Not found')
        
        if not utils.verify(user_credentials.password , user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password, please try again")
        
        access_token =  Oauth2.create_access_token(data = {"user_id" : user.user_id })
        
        return {"access_token":access_token , "token_type" : "Barear", "user_type" : user.user_type}





