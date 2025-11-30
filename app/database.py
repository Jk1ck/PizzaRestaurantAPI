import os
from sqlmodel import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pizza.db")

engine = create_engine(DATABASE_URL, echo=True)