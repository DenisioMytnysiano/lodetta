import uvicorn
from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from api.extensions.utils import get_logger
from database.populate import main as populate_database
from routers import LogoRouter, DetectorRouter

app = FastAPI(
    title="Lodetta",
    description="Simple and easily deployable logo detection API written in Python",
    version="0.1.0"
)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.on_event("startup")
async def startup():
    populate_database()


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to lodetta - simple logo detection API."}


app.include_router(LogoRouter, tags=["Logo"], prefix="/logo")
app.include_router(DetectorRouter, tags=["Detector"], prefix="/detector")

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
