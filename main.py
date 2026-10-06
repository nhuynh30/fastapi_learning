from fastapi import FastAPI
from models import Product

app = FastAPI()


@app.get("/")
def greet():
    return "Welcome bro"

products = [
    Product(id = 1, name = "phone", description= "budget phone", price = 99,  quantity = 10),
    Product(id = 2, name = "laptop", description= "gaming laptop", price=100, quantity= 6)

]

@app.get("/products")
def get__all_products():
    return products