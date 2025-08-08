from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
from .db import init_db, SessionLocal
from .models import LegalDoc, News
from .scrapers.news_fetcher import fetch_all_sources
import datetime as dt
import xml.etree.ElementTree as ET
import os

API_PREFIX = "/api"
app = FastAPI(title="Tax and Technology AM", version="1.0.0")

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Health(BaseModel):
    status: str
    time: str

@app.get(API_PREFIX + "/health", response_model=Health)
def health():
    return Health(status="ok", time=dt.datetime.utcnow().isoformat() + "Z")

class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]

@app.get(API_PREFIX + "/legal/search", response_model=SearchResponse)
def legal_search(q: str):
    db = SessionLocal()
    try:
        hits = db.query(LegalDoc)            .filter((LegalDoc.title.ilike(f"%{q}%")) | (LegalDoc.body.ilike(f"%{q}%")))            .limit(20).all()
        return {
            "query": q,
            "results": [{"id": d.id, "title": d.title, "updated_at": d.updated_at.isoformat(), "snippet": d.body[:240]} for d in hits]
        }
    finally:
        db.close()

@app.get(API_PREFIX + "/news")
def news_feed():
    db = SessionLocal()
    try:
        recs = db.query(News).order_by(News.published_at.desc()).limit(25).all()
        return [
            {"title": r.title, "source": r.source, "url": r.url,
             "published_at": r.published_at.isoformat(), "summary": r.summary or ""}
            for r in recs
        ]
    finally:
        db.close()

@app.post(API_PREFIX + "/cfdi/upload")
async def cfdi_upload(xml: UploadFile = File(...)):
    if not xml.filename.lower().endswith(".xml"):
        raise HTTPException(status_code=400, detail="Archivo no es XML")
    content = await xml.read()
    try:
        root = ET.fromstring(content)
        emisor = root.find(".//{*}Emisor")
        receptor = root.find(".//{*}Receptor")
        total = root.attrib.get("Total") or root.attrib.get("total")
        uuid_el = root.find(".//{*}TimbreFiscalDigital")
        uuid = uuid_el.attrib.get("UUID") if uuid_el is not None else "SIN_UUID"
        data = {
            "uuid": uuid,
            "emisor_rfc": emisor.attrib.get("Rfc") if emisor is not None else "",
            "receptor_rfc": receptor.attrib.get("Rfc") if receptor is not None else "",
            "total": float(total) if total else 0.0
        }
    except Exception:
        raise HTTPException(status_code=400, detail="No se pudieron leer campos del CFDI (demo)")
    return {"status": "ok", "cfdi": data}