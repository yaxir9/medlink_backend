from datetime import datetime , timedelta
from fastapi import Depends, status, HTTPException 
from jose import JWTError , jwt
from fastapi.security import OAuth2PasswordBearer
import schema , db , models
from sqlalchemy.orm import Session 
from config import setting
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='Login')


# SECRET_KEY = "4c075c2c885a9042b38c7547b0f96f96243f15371c07009119353dc99f326012"
# ALGORIHTM  = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 180

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=setting.access_token_expire_minutes)
    to_encode.update({"exp" : expire})
    
    encode_jwt = jwt.encode(to_encode , setting.secret_key  , algorithm= setting.algorithm)
    return encode_jwt

# credentials_axception
def verify_access_token(token : str , credentials_axception ):
    try:
        payload = jwt.decode(token , setting.secret_key , algorithms=[setting.algorithm])
        id : str = payload.get("user_id")
        if id is None : 
            print("Id" , id)
            raise  credentials_axception 
        
        token_data = schema.TokenData(id= id)
    except JWTError:
        print("Error Occured")
        raise credentials_axception
   
    
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme) , db : Session = Depends(db.get_db)):

    # print("Token===> ",token)
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentails", headers = {"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.user_id == token.id).first()

    return user


