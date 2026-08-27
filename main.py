from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from calculator import calculate_future_value

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculationRequest(BaseModel):
    rj: float = Field(gt=-1)
    SK: float = Field(ge=0)
    EM: float = Field(ge=0)
    n: int = Field(gt=0)

@app.get("/")
def root():
    return {"message": "Python Calc API läuft"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Python"}

@app.post("/api/calculate")
def calculate(request: CalculationRequest):
    return calculate_future_value(request.rj, request.SK, request.EM, request.n)