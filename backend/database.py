import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://khanhngoc:reXDPp51z5wYQlx7RoW50hebXS7koPBG@dpg-d50op28gjchc73chm3u0-a.singapore-postgres.render.com/quanly_dongphuc"  # fallback local
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
