from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
import datetime as dt

Base = declarative_base()

class LegalDoc(Base):
    __tablename__ = "legal_docs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    source = Column(String(80), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    published_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    summary = Column(Text, nullable=True)

class CFDI(Base):
    __tablename__ = "cfdi"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(64), unique=True, nullable=False)
    emisor_rfc = Column(String(20), nullable=True)
    receptor_rfc = Column(String(20), nullable=True)
    total = Column(Float, default=0.0)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)