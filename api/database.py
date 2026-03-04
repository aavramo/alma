from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./music.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)
