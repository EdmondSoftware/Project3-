from fastapi import FastAPI, HTTPException

app = FastAPI()

# Mock data: List of cars stored as tuples (id, make, model, year, price)
cars_db = [
    (1, "Toyota", "Camry", 2022, 30000),
    (2, "Honda", "Civic", 2023, 25000),
    (3, "Ford", "Mustang", 2021, 45000),
]

@app.get("/")
def read_root():
    return "Welcome to the Car Dealership API! Use /cars to list available cars or /cars/{id}/price for pricing."

@app.get("/cars")
def list_cars():
    """
    List all available cars.
    """
    return [
        f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Price: ${car[4]:,.2f}"
        for car in cars_db
    ]

@app.get("/cars/{car_id}/price")
def get_car_price(car_id: int):
    """
    Get the price of a specific car by its ID.
    """
    for car in cars_db:
        if car[0] == car_id:
            return f"The price of {car[1]} {car[2]} ({car[3]}) is ${car[4]:,.2f}."
    raise HTTPException(status_code=404, detail="Car not found")

@app.get("/cars/add")
def add_car(id: int, make: str, model: str, year: int, price: float):
    """
    Add a new car to the list using query parameters.
    """
    if any(car[0] == id for car in cars_db):
        raise HTTPException(status_code=400, detail="Car with this ID already exists.")
    cars_db.append((id, make, model, year, price))
    return f"Car {make} {model} ({year}) added successfully with ID {id}."
