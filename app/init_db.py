from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

print("Tables registered:", Base.metadata.tables.keys())
print("Database tables created successfully!")