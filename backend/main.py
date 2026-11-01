from fastapi import FastAPI
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Lab1 API")

# Kích hoạt tính năng thu thập số liệu và mở cổng /metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    # Biến DB_PASSWORD này sau này sẽ do Vault & External Secrets bơm vào Pod
    db_password = os.getenv("DB_PASSWORD", "Not Configured Yet")
    return {
        "message": "Hello from FastAPI Backend!",
        "db_status": "Connected" if db_password != "Not Configured Yet" else "Missing Secret",
        "secret_length": len(db_password) if db_password else 0
    }