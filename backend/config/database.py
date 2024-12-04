from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config.environment import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a database session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
