from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import auth, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Expense Tracker API")

app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}