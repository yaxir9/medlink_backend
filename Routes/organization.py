from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
# from .. import models, schema, utils
import models, schema, utils, Oauth2
from db import  get_db
from sqlalchemy.orm import Session
import traceback
from typing import List
router = APIRouter()
import requests 

# add organization info
@router.post('/add_organization', status_code=status.HTTP_201_CREATED, tags=['Organization'], response_model= schema.organizationOut)
async def Create_Organization(organization : schema.organization, db  : Session = Depends(get_db), current_user : int = Depends(Oauth2.get_current_user)):

    if current_user.user_type == 'organization':
        try:
            new_org = models.Organization(**organization.dict(), user_id=current_user.user_id)
            db.add(new_org)
            db.commit()
            db.refresh(new_org)
            return new_org
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unuthurized user")

#update organization info 
@router.put('/update_organization/{id}', response_model=schema.organizationOut, tags=['Organization'])
async def update_Organization(id: int, organization: schema.organization, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
        if current_user.user_type == 'organization':
            org = db.query(models.Organization).filter(models.Organization.organization_id == id)
            update_org = org.first()
            print("Current_user:", current_user.user_id)
            print("org:", update_org.user.user_id)

            if update_org is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization with ID {id} does not exist")

            if update_org.user.user_id != current_user.user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

            org.update(organization.dict(), synchronize_session=False)
            db.commit()

            return update_org
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action")



    
# delete organization info
@router.delete('/delete_organiztion', status_code=status.HTTP_204_NO_CONTENT, tags=['Organization'])
async def delete_Organization(organization : schema.deleteOrganization, db  : Session = Depends(get_db), current_user : int = Depends(Oauth2.get_current_user)):

    if current_user.user_type == 'organization':
        org = db.query(models.Organization).filter(models.Organization.organization_id == organization.id)
        delete_org = org.first()
        if delete_org == None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"organization with Id : {id} dose not exist")
    
        if delete_org.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")

        deleted_posts = db.query(models.Post).filter(models.Post.organization_id == delete_org.organization_id).delete()
        deleted_employees = db.query(models.Employees).filter(models.Employees.organization_id == delete_org.organization_id).delete()
        org.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no access to perform this action") 

# get single organization
@router.get('/single_organization', response_model=schema.organizationOut, status_code=status.HTTP_200_OK, tags=['Organization'])
async def get_Organization(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

        if current_user.user_type == 'organization':
            org = db.query(models.Organization).filter(models.Organization.user_id == current_user.user_id).first()
            if not org:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization with ID {id} does not exist")
            
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't access this information")
        
        return org
        


#get all the registered organizations info
@router.get('/all_organizations', response_model= List[schema.organizationOut], status_code=status.HTTP_200_OK, tags=['Organization'])
async def all_organizations(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    try:
        orgs = db.query(models.Organization).all()
        return orgs
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
