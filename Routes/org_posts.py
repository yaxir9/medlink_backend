from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List
router = APIRouter()

# create_post
@router.post('/create_posts',response_model=schema.postOut, status_code=status.HTTP_201_CREATED, tags=['Org_Posts'])
async def create_Post(post : schema.post,  db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        if current_user.user_type.lower() == 'organization':
            org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
            # pri
            # print("org id : ",org.organization_id)

            # print(org)
            new_post = models.Post(**post.dict(), organization_id = org.organization_id)
            db.add(new_post)            
            db.commit()
            db.refresh(new_post)
            return new_post
            # return org 
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get_post 
@router.get('/post/{id}', response_model= schema.postOut, status_code=status.HTTP_200_OK, tags=['Org_Posts'])
async def getPost(id : int,  db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
    
        post = db.query(models.Post).filter(models.Post.post_id == id).first()

        if not post:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"post at this {id} dose not exist")
        
        return post 
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# org all post
@router.get('/posts/', response_model= List[schema.postOut], status_code=status.HTTP_200_OK, tags=['Org_Posts'])
async def orgPosts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        
        org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
        if org:
            posts = db.query(models.Post).filter(models.Post.organization_id == org.organization_id).all()
            if not posts:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"post at this {id} dose not exist")
            return posts 
    # else:
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")
# get all posts
@router.get('/allposts/', response_model= List[schema.postOut], status_code=status.HTTP_200_OK, tags=['Org_Posts'])
async def getAllPosts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
    
        posts = db.query(models.Post).all()
        if not posts:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"There is not posts avalible in database")
        return posts

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

# delete post
@router.delete('/deletepost/', response_model= schema.postOut, status_code=status.HTTP_200_OK, tags=['Org_Posts'])
async def deletePost(del_post : schema.deletePost, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        if current_user.user_type.lower() == 'organization':
            post = db.query(models.Post).filter(models.Post.post_id == del_post.id)
            delete_post = post.first()
            if delete_post == None:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"Post with Id : {del_post.id} dose not exist")

        
            if delete_post.organization.user.user_id != current_user.user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
            
            post.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 



# update post data
# 
@router.put('/updatepost/{id}', response_model=schema.postOut, status_code=status.HTTP_200_OK, tags=['Org_Posts'])
async def updatePost(id: int, post: schema.post, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'organization':
        find_post = db.query(models.Post).filter(models.Post.post_id == id)
        update_post = find_post.first()

        if update_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization with ID {id} does not exist")

        if update_post.organization.user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

        updated_post = post.dict()
        updated_post.update({"organization_id": update_post.organization_id})

        find_post.update(updated_post, synchronize_session=False)
        db.commit()

        return update_post
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")


@router.delete('/delete_all_posts', status_code=status.HTTP_201_CREATED, tags=['Org_Posts'])
async def deleteAll(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'organization':
        org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
        
        # Delete all posts with the same organization ID
        deleted_count = db.query(models.Post).filter(models.Post.organization_id == org.organization_id).delete()
        
        # Commit the changes to the database
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")



# ############################ return only those org posts that you are following#######################
# response_model=List[schema.postOut], 
@router.get('/following_org_posts', status_code=status.HTTP_200_OK, tags=['Org_Posts'])
async def get_followed_org_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    if current_user.user_type.lower() == 'nurse' or current_user.user_type.lower() == 'doctor':
        
        professional = db.query(models.Professional).filter(models.Professional.user_id == current_user.user_id).first()

        if professional is None:
            raise HTTPException(status_code=404, detail="Professional not found")
        
        followed_organization_ids = [follow.organization_id for follow in professional.followed]
        job_posts = db.query(models.Post).filter(models.Post.organization_id.in_(followed_organization_ids)).all()

        return [job_post for job_post in job_posts]
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")

