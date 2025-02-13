from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class DetectionData(Base):
    __tablename__ = "detection_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text)

class CountData(Base):
    __tablename__ = "count_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    count_in = Column(Integer, default=0)
    count_out = Column(Integer, default=0)

class ConfigArea(Base):
    __tablename__ = "config_area"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, default="Default Area")
    polygon = Column(Text, default="[]")

def init_db():
    Base.metadata.create_all(bind=engine)
