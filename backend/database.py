from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables (to read DATABASE_URL)
load_dotenv()

# ✅ Get the Postgres URL from your .env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create Engine (Removed SQLite specific "check_same_thread" argument)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()