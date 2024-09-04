from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# Initialize the database
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the models
class Organization(Base):
    __tablename__ = 'organization'
    
    name = Column(String(255), primary_key=True)  # PK
    category = Column(String(255))
    logo_link = Column(String(255))

class User(Base):
    __tablename__ = 'user'
    
    name = Column(String(255), primary_key=True)
    location = Column(String(255))
    organization_name = Column(String(255), ForeignKey('organization.name'))  # FK
    profile_pic = Column(String(255))

# Create tables if not already present
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
