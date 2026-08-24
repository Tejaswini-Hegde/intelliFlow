from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.settings import settings

# 1. Construct the secure Database Connection String URL
DATABASE_URL = (
    f"postgresql://{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
)

# 2. Create the SQL Alchemy Engine (Connection Pool Manager)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Automatically checks and recovers broken database links
)

# 3. Create a Session Factory for handling transaction blocks
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Define the Base class that all database tables will inherit from later
Base = declarative_base()

# 5. Dependency Injector helper function to open and close connections safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()