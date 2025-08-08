from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, LegalDoc, News
import datetime as dt

engine = create_engine("sqlite:///./taxtech.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(LegalDoc).count() == 0:
            samples = [
                ("Código Fiscal de la Federación - Art. 29-A", "Requisitos de los CFDI. Texto de ejemplo para demo."),
                ("Ley del IVA - Tasa general", "La tasa general del IVA es 16%. Texto de ejemplo para demo."),
                ("RMF 2025 - Reglas CFDI", "Reglas aplicables a CFDI. Texto de ejemplo para demo.")
            ]
            for t, b in samples:
                db.add(LegalDoc(title=t, body=b, updated_at=dt.datetime.utcnow()))
            db.commit()
        if db.query(News).count() == 0:
            db.add(News(title="Bienvenido a Tax and Technology AM", source="Sistema", url="https://example.com",
                        published_at=dt.datetime.utcnow(), summary="Feed listo. Se poblará con fuentes reales en producción."))
            db.commit()
    finally:
        db.close()