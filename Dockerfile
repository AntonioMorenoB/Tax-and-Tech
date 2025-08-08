# Build frontend
FROM node:20-slim AS webbuild
WORKDIR /app
COPY frontend/package.json frontend/tsconfig.json frontend/next.config.js ./
RUN npm install
COPY frontend ./
RUN npm run build && npm run export

# Backend runtime
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY --from=webbuild /app/out ./app/static
ENV PORT=8080
EXPOSE 8080
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]