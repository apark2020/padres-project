from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase
from config import Config
from app import app, db

engine = Config.SQLALCHEMY_DATABASE_URI

with app.app_context():
    db.reflect()

class Base(DeclarativeBase):
    pass

class PitchData(Base):
    __table__ = db.metadata.tables["pitch_data"]