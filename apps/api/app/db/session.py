from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # Assuming settings contains the database URL

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base class for models
from sqlalchemy.orm import declarative_base

Base = declarative_base()