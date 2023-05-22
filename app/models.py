"""
CHECK THIS TUTORIAL!!!!!
Taken from: https://fastapi.tiangolo.com/tutorial/sql-databases/
"""
import enum
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime, Date, Time, Float
from sqlalchemy.orm import relationship, backref
from .database import Base

# MANY TO MANY RELATIONSHIP
# USER PLANTS IS THE ASSOCIATION TABLE

class Category(enum.Enum):
    """PLANTS CATEGORY"""
    fruit = "fruit"
    vegetable = "vegetable"
    tree = "tree"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    hashed_pass = Column(String, nullable=False)
    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    plants = relationship("UserPlants", back_populates="users")
    # plants_harvested = relationship("UserPlantsHarvested", back_populates="users")


class Plant(Base):
    __tablename__ = "plant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(Enum(Category), index=True, default = Category.fruit)
    p_info = Column(String, nullable=False)
    min_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_humidity = Column(Float, nullable=False)
    max_humidity = Column(Float, nullable=False)
    min_rain_tolerance = Column(Float, nullable=False)
    max_rain_tolerance = Column(Float, nullable=False)
    min_planting_time = Column(Integer, nullable=False)
    max_planting_time = Column(Integer, nullable=False)
    summer = Column(Boolean, nullable=False)
    rainy_season = Column(Boolean, nullable=False)
    file_path = Column(String, nullable= True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class UserPlants(Base):
    __tablename__ = "user_plants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    plant_id = Column(Integer, ForeignKey("plant.id"))
    is_harvested = Column(Boolean, default = False)
    date_planted = Column(Date, default=datetime.datetime.now)
    min_date_estimate_harvest = Column(Date) # date_planted + min_planting time
    max_date_estimate_harvest = Column(Date) # date_planted + max_planting time (pag lampas na sa max and ala pa rin update auto harvest)
    date_harvested = Column(Date, nullable=True) # for now wala pa pero magkalaman once na magtrue ang is_harvested
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    users = relationship("User", back_populates="plants")
    description = relationship("Plant", backref=backref("info", lazy="joined"))



# class UserPlantsHarvested(Base):
#     __tablename__ = "user_plants_harvested"


#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     plant_id = Column(Integer, ForeignKey("plant.id"))
#     date_harvested = 
#     created_at = Column(DateTime, default=datetime.datetime.now)
#     updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

#     users = relationship("User", back_populates="plants_harvested")
#     description = relationship("Plant", backref=backref("info_h", lazy="joined"))

