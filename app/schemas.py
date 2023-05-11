"""
Schema file

Ang ibig sabihin lang neto, eto ung format nung mga marereturn or makukuhang data.


"""
import datetime
from typing import Optional, Annotated, Union
from pydantic import BaseModel
from fastapi import Query

class PlantsResponse(BaseModel):
	id: int
	name: str = None
	category: str
	p_info: str = None 
	min_temp: float = None
	max_temp: float = None
	min_humidity: float = None
	max_humidity: float = None
	rain_tolerance: float = None
	planting_time: int = None
	summer: bool = False
	rainy_season: bool = False

	class Config:
		orm_mode = True

class PlantRequest(BaseModel):
	name: str = None  
	category: str = None
	p_info: str = None 
	min_temp: float = None
	max_temp: float = None
	min_humidity: float = None
	max_humidity: float = None
	rain_tolerance: float = None 
	planting_time: int = None
	summer: bool = None
	rainy_season: bool = None

# class UserPlantsRequest(BaseModel):

class CurrentUserPlants(BaseModel):
	plants: list[PlantsResponse]

	class Config:
		orm_mode = True	

class UserRequest(BaseModel):
	username: str = None
	birthday: Optional[datetime.date] = None
	hashed_pass1: str = None
	hashed_pass2: str = None
	province: str = None
	city: str = None
	is_active: bool = False
	is_public: bool = True
	plants: Optional[list[int]]


# same for update
class UserResponse(BaseModel):
	id: int
	username: str = None
	birthday: Optional[datetime.date] = None
	# hashed_pass: str = None
	province: str = None
	city: str = None
	is_active: bool= False
	is_public: bool = True
	plants: list[PlantsResponse]

	class Config:
		orm_mode = True	


class UserFilterRequest(BaseModel):
	upperAge: Optional[int] = None 
	lowerAge: Optional[int] = None
	province: Optional[str] = None
	city: Optional[str] = None
	is_active: Optional[bool] = None
	is_public: Optional[bool] = None

class UserUpdateRequest(BaseModel):
	birthday: datetime.date = None
	province: str = None
	city: str = None
	is_public: bool = None


class UserChangePass(BaseModel):
	old_pass: str = None
	new_pass1: str = None
	new_pass2: str = None


class PlantUpdate(BaseModel):
	name: str = None
	category: str
	p_info: str = None
	min_temp: float = None
	max_temp: float = None
	min_humidity: float = None
	max_humidity: float = None
	rain_tolerance: float = None
	planting_time: int = None
	summer: bool = None
	rainy_season: bool = None

class PlantFilterRequest(BaseModel):
	category: Optional[str] = None
	upper_p_time: Optional[int] = None
	lower_p_time: Optional[int] = None
	summer: Optional[bool] = None
	rainy_season: Optional[bool] = None