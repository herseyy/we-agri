"""
CHECK THIS TUTORIAL!!!!!
Taken from: https://fastapi.tiangolo.com/tutorial/sql-databases/
"""
import enum
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime, Date, Time
from sqlalchemy.orm import relationship, backref
from .database import Base

# MANY TO MANY RELATIONSHIP
# USER PLANTS IS THE ASSOCIATION TABLE

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    birthday = Column(Date, nullable=True)
    hashed_pass = Column(String, nullable=False)
    province = Column(String, nullable=False)
    city = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    plants = relationship("UserPlants", back_populates="users")


class Plant(Base):
    __tablename__ = "plant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    min_temp = Column(Integer, nullable=False)
    max_temp = Column(Integer, nullable=False)
    min_humidity = Column(Integer, nullable=False)
    max_humidity = Column(Integer, nullable=False)
    rain_tolerance = Column(Integer, nullable=False)
    planting_time = Column(Integer, nullable=False)
    summer = Column(Boolean, nullable=False)
    rainy_season = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserPlants(Base):
    __tablename__ = "user_plants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    plant_id = Column(Integer, ForeignKey("plant.id"))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    users = relationship("User", back_populates="plants")
    description = relationship("Plant", backref=backref("info", lazy="joined"))