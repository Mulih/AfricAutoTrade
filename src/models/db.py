from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.settings.config import settings

print("-> Database URL:", settings.database_url)
# Create a new SQLAlchemy engine instance

engine = create_engine(settings.database_url, echo=True, future=True)
# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()