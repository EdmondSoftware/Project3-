from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for a car
class Car(BaseModel):
    id: int
    make: str
    model: str
    year: int
    price: float

# In-memory database of cars
cars_db = [
    Car(id=1, make="Toyota", model="Camry", year=2022, price=30000),
    Car(id=2, make="Honda", model="Civic", year=2023, price=25000),
    Car(id=3, make="Ford", model="Mustang", year=2021, price=45000),
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Dealership API!"}

@app.get("/cars", response_model=List[Car])
def list_cars():
    """List all available cars."""
    return cars_db

@app.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    """Retrieve details of a car by its ID."""
    for car in cars_db:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")

@app.get("/cars/{car_id}/price")
def get_car_price(car_id: int):
    """Retrieve the price of a car by its ID."""
    for car in cars_db:
        if car.id == car_id:
            return {"id": car.id, "make": car.make, "model": car.model, "price": car.price}
    raise HTTPException(status_code=404, detail="Car not found")

@app.post("/cars", response_model=Car)
def add_car(car: Car):
    """Add a new car to the database."""
    if any(existing_car.id == car.id for existing_car in cars_db):
        raise HTTPException(status_code=400, detail="Car with this ID already exists")
    cars_db.append(car)
    return car
