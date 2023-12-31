 #!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight

router = APIRouter()

@router.post("/", response_description="Post a new flight", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(request: Request, flight: Flight = Body(...)):
    flight = jsonable_encoder(flight)
    new_flight = request.app.database["flight"].insert_one(flight)
    created_flight = request.app.database["flight"].find_one(
        {"_id": new_flight.inserted_id}
    )
    return created_flight

@router.get("/", response_description="Get all flights", response_model=List)
def list_books(request: Request, option:str, option_chosen:str):
    if option == "airline":
        group = [{"$match": {"airline": option_chosen, "age":{"$gte": 18}, "reason": {"$in":["On vacation/Pleasure", "Business/Work"]}, "transit":{"$nin":["Own car"]}}},
                 {"$project": {"id": "$_id", "airline": 1, "From": 1, "to": 1, "day": 1, "month": 1, "year": 1, "age": 1, "gender": 1, "reason": 1, "stay": 1, "transit": 1, "connection": 1, "wait": 1}},
                 {"$sort": {"month": -1}}]
    elif option == "airport":
        group = [{"$match": {"to": option_chosen, "connection": "False", "age":{"$gte": 18}, "reason": {"$in":["On vacation/Pleasure", "Business/Work"]}, "transit":{"$nin":["Own car"]}}},
                 {"$project": {"id": "$_id", "airline": 1, "From": 1, "to": 1, "day": 1, "month": 1, "year": 1, "age": 1, "gender": 1, "reason": 1, "stay": 1, "transit": 1, "connection": 1, "wait": 1}},
                 {"$sort": {"month": -1}}]
    pipeline = list(request.app.database["flight"].aggregate(group))
    return pipeline
