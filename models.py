from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime, func,Date
from sqlalchemy.sql.expression import text 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship 
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    professional = relationship("Professional", uselist=False, back_populates='user')
    userImage = relationship("UserImage", uselist=False, back_populates='user')
    patient = relationship("Patient", uselist=False, back_populates="user")
    organization = relationship("Organization", uselist=False, back_populates="user")

class UserImage(Base):
    __tablename__ = 'userImages'
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=date.today) 

    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    user = relationship("User", back_populates="userImage")

class Professional(Base):
    __tablename__ = 'professionals'
    professional_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    intern_status = Column(Boolean, nullable=False)
    current_position = Column(String, nullable=False)
    address = Column(String, nullable=False)
    part_time = Column(Boolean, nullable=False)

    registeration_no = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    user = relationship("User", back_populates="professional")

    reviews = relationship("Reviews", back_populates="professional")
    qualifications = relationship("Qualification", back_populates="professional")
    experience = relationship("Experience", back_populates="professional")
    applications = relationship("Application", back_populates='professional')
    followed =  relationship("Follow", back_populates='professional')
class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    user = relationship("User", back_populates="patient")

    reviews = relationship("Reviews", back_populates="patient")

class Qualification(Base):
    __tablename__ = 'qualification'
    qualification_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    degree = Column(String, nullable=False)
    college = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    completion_date = Column(Date, nullable=False)

    professional_id = Column(Integer, ForeignKey('professionals.professional_id'), nullable=False)
    professional = relationship("Professional", back_populates="qualifications")

class Experience(Base):
    __tablename__='experience'
    experience_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    professional_id = Column(Integer, ForeignKey('professionals.professional_id'), nullable=False)
    professional = relationship("Professional", back_populates="experience")

class Organization(Base):
    __tablename__ = 'organization'
    organization_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    org_type = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    address = Column(String, nullable=False)
    
    employees = relationship("Employees", back_populates="organization")
    posts = relationship("Post", back_populates="organization")
    follower = relationship("Follow", back_populates="organization")

    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    user = relationship("User", back_populates="organization")

class Employees(Base):
    __tablename__='employees'
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    timming = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    organization_id = Column(Integer, ForeignKey('organization.organization_id'), nullable=False)
    organization = relationship("Organization", back_populates="employees")

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    job_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    
    
    organization_id = Column(Integer, ForeignKey('organization.organization_id'), nullable=False)
    organization = relationship("Organization", back_populates="posts")
    deadline = Column(Date, default=date.today, nullable=False)
    date = Column(Date, nullable=False, default=date.today)

    applications = relationship("Application", back_populates="post")

class Application(Base):
    __tablename__ = 'applications'
    application_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    professional_id = Column(Integer, ForeignKey('professionals.professional_id'), nullable=False)
    date = Column(Date, default=date.today, nullable=False)

    post = relationship("Post", back_populates="applications")
    professional = relationship("Professional", back_populates="applications")

class Reviews(Base):
    __tablename__ = 'reviews'
    reviews_id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    professional_id = Column(Integer, ForeignKey('professionals.professional_id'), nullable=False)
    professional = relationship("Professional", back_populates="reviews")

    patient_id = Column(Integer, ForeignKey('patients.patient_id'), nullable=False)
    patient = relationship("Patient", back_populates="reviews")


class Follow(Base):
    __tablename__='follow'
    follow_id =Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey('organization.organization_id'), nullable=False)
    organization = relationship("Organization", back_populates="follower")
    professional_id = Column(Integer, ForeignKey('professionals.professional_id'), nullable=False)
    professional = relationship("Professional", back_populates="followed")
    date = Column(Date, default=date.today, nullable=False)