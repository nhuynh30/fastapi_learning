from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods=['*']
)




@app.get("/")
def greet():
    return "Welcome bro"

database_models.Base.metadata.create_all(bind=engine)

products = [
    Product(id = 1, name = "phone", description= "budget phone", price = 99,  quantity = 10),
    Product(id = 2, name = "laptop", description= "gaming laptop", price=100, quantity= 6)

]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

def init_db():
    db = SessionLocal()

    count = db.query(database_models.Product).count()

    try: 
        if count == 0:
            for product in products: 
                db.add(database_models.Product(**product.model_dump()))
            
            db.commit()
    finally:
        db.close()


init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
        
    

    return "product not found"


@app.post("/products")
def add_product(x: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**x.model_dump()))
    db.commit()
    return x


@app.put("/products/{id}")
def update_product(id : int, product: Product, db : Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product is None:
        return "Product not exist"
    else:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price  =product.price
        db_product.quantity = product.quantity

        db.commit()
        return "Product updated"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "No product found"