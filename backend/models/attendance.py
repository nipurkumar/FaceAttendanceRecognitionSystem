from sqlalchemy import Column, Integer, String, DateTime, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    department = Column(String(100))
    registered_date = Column(DateTime, default=datetime.utcnow)
    face_encoding = Column(String)
    profile_image = Column(String)
    
    attendances = relationship("Attendance", back_populates="user")

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    date = Column(Date, nullable=False)
    confidence = Column(Float)
    location = Column(String(100))
    device_id = Column(String(50))
    
    user = relationship("User", back_populates="attendances")

class AttendanceStatistics(Base):
    __tablename__ = 'attendance_statistics'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Integer, default=0)
    present_days = Column(Integer, default=0)
    absent_days = Column(Integer, default=0)
    late_days = Column(Integer, default=0)
    attendance_percentage = Column(Float, default=0.0)