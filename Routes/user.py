from fastapi import FastAPI, Response, APIRouter, status, HTTPException, Depends, UploadFile, File
# from .. import models, schema, utils
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
from pathlib import Path
import os


router = APIRouter()

@router.post('/create_user' , status_code=status.HTTP_201_CREATED, response_model=schema.userOut, tags=["User"] )
def create_user( user : schema.UserCreate, db : Session = Depends(get_db)):
    try:
        print("Create User.")
        hashed_password = utils.hash(user.password)
        print("hash_password : ",hashed_password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# all employees


@router.get('/user/{id}' , response_model= schema.userOut, tags=["User"])
async def get_user(id : int , db : Session = Depends(get_db)):
    try:

        user = db.query(models.User).filter(models.User.user_id == id).first()
        if not user :
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"user at {id} this id dose not exist")
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# all employees

@router.delete('/delete_user', status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
async def delete_user(user : schema.delteUser, db : Session = Depends(get_db), current_user : int = Depends(Oauth2.get_current_user)):
    try:
        user = db.query(models.User).filter(models.User.user_id == user.id)
        delete_user = user.first()

        if delete_user == None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"post with Id : {id} dose not exist")
        
        if delete_user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
        
        user.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# all employees


# ###########################Add Profile Images ###########################################


@router.post('/profileImage', status_code=status.HTTP_201_CREATED, tags=["UserImage"])
async def add_image( file: UploadFile = File(...), db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are allowed.")

        save_path = Path('static') / 'user'
        save_path.mkdir(parents=True, exist_ok=True)

        file_path = save_path / f"{current_user.user_id}.{file.filename.split('.')[-1]}"
        with file_path.open('wb') as buffer:
            buffer.write(await file.read())

        image = models.UserImage(path=str(file_path), user_id=current_user.user_id)
        db.add(image)
        db.commit()
        db.refresh(image)

        return {"path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# update profileImage

@router.put('/updateProfile', status_code=status.HTTP_200_OK, tags=["UserImage"])
async def update_image( file: UploadFile = File(...), db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are allowed.")

        save_path = Path('static') / 'user'
        save_path.mkdir(parents=True, exist_ok=True)

        # Get the old image path from the database
        old_image = db.query(models.UserImage).filter(models.UserImage.user_id == current_user.user_id).first()
        if old_image:
            # Delete the old image file
            os.remove(old_image.path)
            # Remove the old image from the database
            db.delete(old_image)
            db.commit()

        # Save the new image
        file_path = save_path / f"{current_user.user_id}.{file.filename.split('.')[-1]}"
        with file_path.open('wb') as buffer:
            buffer.write(await file.read())

        # Create a new entry in the database for the updated image
        image = models.UserImage(path=str(file_path), user_id=current_user.user_id)
        db.add(image)
        db.commit()
        db.refresh(image)

        return {"path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.delete('/delete_userimage', status_code=status.HTTP_204_NO_CONTENT, tags=["UserImage"])
async def delete_userImage(userImage : schema.delteUser, db : Session = Depends(get_db), current_user : int = Depends(Oauth2.get_current_user)):
    try:
        user_image = db.query(models.UserImage).filter(models.UserImage.image_id == userImage.id)
        delete_user_image = user_image.first()

        if delete_user_image == None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"post with Id : {id} dose not exist")
        print("delete_user_image : ",delete_user_image.user_id)
        print("delete_user_image  image_id : ",delete_user_image.image_id)
        print("current usre : ",current_user.user_id )
        if delete_user_image.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
        
        user_image.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# all employees


@router.get('/userImage/{id}' , response_model= schema.userImageOut, tags=["User"])
async def get_user(id : int , db : Session = Depends(get_db),current_user : int = Depends(Oauth2.get_current_user)):
    try:
        userImage = db.query(models.UserImage).filter(models.UserImage.image_id == id).first()
        if not userImage :
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"user at {id} this id dose not exist")    
        return userImage
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# all employees


# ############################

@router.get("/getUserImage/{filename}", status_code=status.HTTP_200_OK, tags=['User'])
async def get_user_image(filename: str, current_user : int = Depends(Oauth2.get_current_user)):
    try:
        print("filename",filename)
        return FileResponse(filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# all employees