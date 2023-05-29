from typing import Annotated
from datetime import datetime, timedelta
import uuid

import jwt

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import UUID
from db import ALGORITHM, SECRET_KEY, SessionLocal, User, db_create_user, db_get_user, db_get_user_by_email, db_get_user_by_phone
from notifications import create_sms_client, send_top, whitelist_phone_number

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

sms_client = create_sms_client()

class CustomerBase(BaseModel):
    phone_number: int
    password: str

    class Config:
        orm_mode = True


class AdminBase(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class CustomerRegistration(CustomerBase):
    national_id: int

    class Config:
        orm_mode = True

@app.post("/otp/send/{phone_number}")
def generate_otp(phone_number: int):
    try: 
        send_top(sms_client, phone_number)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="failed to send OTP")
    return {"message": "OTP sent successfully"}

@app.post("/otp/whitelist_phone_number/{phone_number}")
def whitelist_otp_phone_number(phone_number: int):
    try: 
        whitelist_phone_number(sms_client, phone_number)
    except Exception:
        raise HTTPException(status_code=400, detail="failed to whitelist phone number")
    return {"message": "successfully whitelisted phone number"}

@app.post("/customer/registration")
def customer_registration(reg: CustomerRegistration, db: Session = Depends(get_db)):
    db_user = db_get_user_by_phone(db=db, phone_number=reg.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    user = User(id=uuid.uuid4(), phone_number=reg.phone_number, national_id=reg.national_id, password=reg.password)
    try:
        return db_create_user(db=db, user=user)
    except Exception:
        raise HTTPException(status_code=500, detail="something went wrong")



@app.post("/admin/registration")
def admin_registration(reg: AdminBase, db: Session = Depends(get_db)):
    db_user = db_get_user_by_email(db=db, email=reg.email.__str__().lower())
    if db_user:
        raise HTTPException(status_code=400, detail="user already registered")
    user = User(
        id=uuid.uuid4(), email=reg.email.__str__().lower(), password=reg.password
    )
    return db_create_user(db=db, user=user)


@app.post("/admin/login")
def admin_login(reg: AdminBase, db: Session = Depends(get_db)):
    try:
        db_user = db_get_user_by_email(db=db, email=reg.email.__str__().lower())
    except Exception:
        raise HTTPException(status_code=500, detail="something went wrong")

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.password.__str__() != reg.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    encoded = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(seconds=1800),
            "role": db_user.user_type.__str__(),
            "uuid": str(db_user.id),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return jsonable_encoder(encoded)


@app.post("/customer/login")
def customer_login(reg: CustomerBase, db: Session = Depends(get_db)):
    db_user = db_get_user_by_phone(db=db, phone_number=reg.phone_number)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if db_user.password.__str__() != reg.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    encoded = jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(seconds=1800),
            "role": db_user.user_type.__str__(),
            "uuid": str(db_user.id),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return jsonable_encoder(encoded)


@app.get("/me")
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uuid: UUID = payload.get("uuid")
        if user_uuid is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db_get_user(db, user_uuid)
    if user is None:
        raise credentials_exception
    return user


@app.get("/verify-token")
def verify_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uuid: UUID = payload.get("uuid")
        if user_uuid is None:
            return {"valid": False}
    except Exception:
        return {"valid": False}
    user = db_get_user(db, user_uuid)
    if user is None:
        return {"valid": False}
    return {"valid": True}
