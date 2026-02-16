# app/main.py
from fastapi import FastAPI
import json
from pydantic import BaseModel, ConfigDict
from app.optimiser import run_job
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Optimiser API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

schedule_example = json.load(open("schedule.json", "r"))

class SchedulePayload(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            schedule_example
        ]
    })
    T:  dict[int, float]
    I:  dict[int, float]
    ST: dict[int, int]
    OV_limit: dict[str, int] | None = None
    d:  dict[str, dict[str, int]]
    e:  dict[str, dict[str, int]]

@app.post("/solve")
async def solve(payload: SchedulePayload):
    """
    POST the JSON; get back figure + stats synchronously
    (good enough for local testing; switch to BackgroundTasks/Celery later).
    """
    result = run_job(payload.model_dump())
    return result

@app.get("/")
def root():
    return {"msg": "Up & running 🎉  – hit /docs for Swagger UI"}
