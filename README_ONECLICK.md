# Tax and Technology AM — One Click Web (Single Service)

**Cómo desplegar en Render (gratis):**
1) Sube este folder a un repo en GitHub (root con `Dockerfile`, `render.yaml`, `backend/`, `frontend/`).
2) En https://render.com → New → Blueprint → selecciona tu repo.
3) Render lee `render.yaml` y crea un Web Service.
4) Espera ~3–5 min. URL pública: `https://tax-and-tech-am.onrender.com` (o similar).
5) Pruebas: `/api/health`, `/api/news`, `/api/legal/search?q=IVA`, `/api/cfdi/upload`.

**Notas**: Single container (Next export + FastAPI). Evita "Not Found" sirviendo `index.html` en `/` y API en `/api/*`.