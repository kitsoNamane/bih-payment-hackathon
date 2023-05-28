from sqlalchemy import UUID, Boolean, Column, Integer, String
from sqlalchemy.types import DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

SECRET_KEY = "asdfjlkaasdf"
ALGORITHM = "HS256"

DATABASE_URL = "postgresql+psycopg2://postgres:ZAHkX5jKHY7JRkVbB19t@containers-us-west-175.railway.app:6034/railway"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Payments model created below
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service = Column(String, index=True)
    reference = Column(String, unique=True, index=True)
    due_date = Column(DateTime)
    paid_status = Column(Boolean, index=True, default=False)
    payer_id = Column(Integer, unique=False, index=True)
    created_at = Column(DateTime)


def create_payment(db: Session, payment: Payment):
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_all_customer_payments(db: Session, omang_id: int):
    return db.query(Payment).filter(Payment.payer_id == omang_id).first()


def get_all_payments_of_particular_service(db: Session, payment_service: str):
    return (
        db.query(Payment)
        .filter(Payment.service.lower() == payment_service.lower())
        .all()
    )


def get_three_pending_tickets(db: Session, omang_id: int, limit: int = 3):
    return db.query(Payment).filter(Payment.payer_id == omang_id).limit(limit).all()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    phone_number = Column(Integer, unique=True, index=True)
    national_id = Column(Integer, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    user_type = Column(
        Enum("customer", "admin", "super_admin", name="user_type"), default="customer"
    )


def db_get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def db_get_user_by_phone(db: Session, phone_number: int):
    return db.query(User).filter(User.phone_number == phone_number).first()


def db_get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email.lower()).first()


def db_get_user(db: Session, uuid: UUID):
    return db.query(User).filter(User.id == uuid).first()


def db_create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
