from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from app.core.config import SANDBOX_DATABASE_URL

# Engine for the main database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Engine for the sandbox database
sandbox_engine = create_engine(SANDBOX_DATABASE_URL)
SandboxSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sandbox_engine)

# Base class for models
Base = declarative_base()