from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import Config

# Engine for the main database
engine = create_engine(Config.DATABASE_URL)
# Base class for models
Base = declarative_base()
# SessionLocal class for the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

