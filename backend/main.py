from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Flowwork HR API"}


