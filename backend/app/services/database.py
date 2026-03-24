from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("postgresql://postgres.jmwvxjkaaezavqqtvhff:MhdvoSvC9WGKb8P7@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres")

engine = create_engine("postgresql://postgres.jmwvxjkaaezavqqtvhff:MhdvoSvC9WGKb8P7@aws-1-ap-northeast-1.pooler.supabase.com:5432/postgres")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()