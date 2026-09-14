from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import database_models
from database import SessionLocal, engine
from models import Product, ProductCreate

app = FastAPI(title="Learn FastAPI Products API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


initial_products = [
    {"id": 1, "name": "phone", "description": "good phone", "price": 100.00, "quantity": 3},
    {"id": 2, "name": "laptop", "description": "good laptop", "price": 500.00, "quantity": 10},
    {"id": 3, "name": "mouse", "description": "good mouse", "price": 10.00, "quantity": 320},
    {"id": 4, "name": "headphone", "description": "good headphone", "price": 1500.00, "quantity": 220},
]


def seed_database():
    db = SessionLocal()
    try:
        count = db.query(database_models.Product).count()
        if count == 0:
            for item in initial_products:
                db.add(database_models.Product(**item))
            db.commit()
    finally:
        db.close()


seed_database()


@app.get("/")
def greet() -> dict[str, str]:
    return {"message": "Hello from FastAPI"}


@app.get("/products", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)) -> list[Any]:
    return db.query(database_models.Product).all()


@app.get("/product/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@app.post("/product", response_model=Product, status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    new_product = database_models.Product(**product.model_dump(exclude_none=True))
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/product/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    for key, value in product.model_dump(exclude_none=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}