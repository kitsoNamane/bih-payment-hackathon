from datetime import datetime, timedelta
import uuid

import jwt

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import Session

# PGPASSWORD=ZAHkX5jKHY7JRkVbB19t psql -h containers-us-west-175.railway.app -U postgres -p 6034 -d railway

KEY="asdfjlkaasdf"

DATABASE_URL = "postgresql+psycopg2://postgres:ZAHkX5jKHY7JRkVbB19t@containers-us-west-175.railway.app:6034/railway"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Customer(Base):
    __tablename__ = "customer"

    id = Column(UUID, primary_key=True, index=True)
    phone_number = Column(Integer, unique=True, index=True)
    national_id = Column(Integer, unique=True, index=True)
    password = Column(String)

class UserBase(BaseModel):
    phone_number: int
    password: str

    class Config:
        orm_mode = True

class Registration(UserBase):
    national_id: int

    class Config:
        orm_mode = True

def db_get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()

def db_get_customer(db: Session, phone_number: int):
    return db.query(Customer).filter(Customer.phone_number == phone_number).first()

def db_create_user(db: Session, customer: Customer):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@app.post("/registration")
def registration(reg: Registration, db: Session = Depends(get_db)):
    db_customer = db_get_customer(db=db, phone_number=reg.phone_number)
    if db_customer:
        raise HTTPException(status_code=400, detail="customer already registered")
    customer = Customer(id=uuid.uuid4(), phone_number=reg.phone_number, national_id=reg.national_id, password=reg.password)
    return db_create_user(db=db, customer=customer)

@app.post("/login")
def login(reg: UserBase, db: Session = Depends(get_db)):
    db_customer = db_get_customer(db=db, phone_number=reg.phone_number)
    if db_customer is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_customer.password.__str__() != reg.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    encoded = jwt.encode(
        {"exp": datetime.utcnow() + timedelta(seconds=30), "role": "customer"},
        KEY, algorithm="HS256"
    )
    return jsonable_encoder(encoded)


@app.get("/customers")
def get_customers():
    pass
