from fastapi import FastAPI
from models import Product
from database import SessionLocal, engine
import database_models

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Welcome bro"

database_models.Base.metadata.create_all(bind=engine)

products = [
    Product(id = 1, name = "phone", description= "budget phone", price = 99,  quantity = 10),
    Product(id = 2, name = "laptop", description= "gaming laptop", price=100, quantity= 6)

]


def init_db():
    db = SessionLocal()

    for product in products:
        db.add(database_models.Product(**product.model_dump()))

    db.commit()

   
init_db()

@app.get("/products")
def get_all_products():
    db = SessionLocal()
    try:
        return db.query(database_models.Product).all()
    finally:
        db.close()


@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product

    return "product not found"


@app.post("/product")
def add_product(x: Product):
    products.append(x)
    return x


@app.put("/product/{id}")
def update_product(id : int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updtated successfully"

    return "Product not found"


@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]

            return "Deleted successfully"

    return "No product found"