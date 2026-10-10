from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from .config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(50), nullable=False)
    intensity = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    plans = relationship("Plan", back_populates="user", cascade="all, delete-orphan")

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=False)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="plans")

def init_db():
    Base.metadata.create_all(bind=engine)

def save_user(data):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.user_id == data.user_id).first()
        if existing:
            existing.name = data.name
            existing.age = data.age
            existing.weight = data.weight
            existing.goal = data.goal
            existing.intensity = data.intensity
            db.commit()
            db.refresh(existing)
            return existing
        user = User(
            user_id=data.user_id, name=data.name, age=data.age,
            weight=data.weight, goal=data.goal, intensity=data.intensity
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def save_plan(user_pk, original_plan, nutrition_tip):
    db = SessionLocal()
    try:
        plan = Plan(user_id=user_pk, original_plan=original_plan, nutrition_tip=nutrition_tip)
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    finally:
        db.close()

def get_user(user_id):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    finally:
        db.close()

def get_latest_plan(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None, None
        plan = db.query(Plan).filter(Plan.user_id == user.id).order_by(Plan.id.desc()).first()
        return user, plan
    finally:
        db.close()

def update_plan(plan_id, updated_plan, feedback):
    db = SessionLocal()
    try:
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if plan:
            plan.updated_plan = updated_plan
            plan.feedback = feedback
            plan.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(plan)
        return plan
    finally:
        db.close()

def get_all_users():
    db = SessionLocal()
    try:
        return db.query(User).order_by(User.created_at.desc()).all()
    finally:
        db.close()
