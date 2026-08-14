from fastapi import FastAPI

from read_api import router as read_router
from trace_api import router as trace_router
from fixture_endpoint import router as fixture_router

app = FastAPI(title="Manufacturing Neo4j API")

app.include_router(read_router)
app.include_router(trace_router)
app.include_router(fixture_router)

@app.get("/")
def health():
    return {"status": "API running"}
