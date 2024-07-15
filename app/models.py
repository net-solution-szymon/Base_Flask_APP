from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from flask_login import UserMixin
from typing import List
from sqlalchemy.sql import func

from . import db



class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(512))
    role: Mapped[str] = mapped_column(String(50), default='user')
 

