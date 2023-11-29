from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine
from config.config import DB_USER, DB_HOST, DB_NAME, DB_PORT, DB_PASSWORD


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

metadata = MetaData()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# database = databases.Database(DATABASE_URL)
# engine = create_engine(DATABASE_URL)
