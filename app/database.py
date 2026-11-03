import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
            SELECT current_database(), current_schema()
            """))

            print("Connected database:", result.fetchone())

    except Exception as error:
        print("Database Connection Failed!")
        print(error)

# def create_tables():
#     from app import models
#
#     print("Connected database:", engine.url.database)
#     print("Registered tables:", Base.metadata.tables.keys())
#
#     Base.metadata.create_all(bind=engine)
#
#     print("Database tables created successfully!")
