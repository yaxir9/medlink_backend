from fastapi import FastAPI, Depends
import schema, models 
from db import engine ,get_db
from sqlalchemy.orm import Session
from Routes import Auth
from Routes import user, Auth, organization, org_posts,employee, professional, qualification, experience, application,followers, patient, reviews
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = ["*"]  # Allows all origins

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (e.g., GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

models.Base.metadata.create_all(bind= engine)

@app.get('/')
def Hello():
    return {"Message" : "Hello Wrold"}

# git commit -m "update experience and qualification models v2"


app.include_router(user.router)
app.include_router(Auth.router)
app.include_router(organization.router)
app.include_router(org_posts.router)
app.include_router(employee.router)
app.include_router(professional.router)
app.include_router(qualification.router)
app.include_router(experience.router)
app.include_router(application.router)
app.include_router(followers.router)
app.include_router(patient.router)
app.include_router(reviews.router)
