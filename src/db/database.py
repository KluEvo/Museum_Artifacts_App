import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import settings

logger = logging.getLogger(__name__)

logger.info("Initializing database engine")

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
