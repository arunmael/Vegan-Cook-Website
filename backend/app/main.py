from fastapi import FastAPI

from backend.app.db import check_database_connection

app = FastAPI(title="Vegan Cook Website")


@app.get("/api/health")
def health_check():
    check_database_connection()

    return {
        "status": "ok",
        "database": "reachable",
    }
