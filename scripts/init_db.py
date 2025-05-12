from src.models.db import engine, Base
import src.models.db_models # registers models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")