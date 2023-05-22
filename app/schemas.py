"""
Schema file

Ang ibig sabihin lang neto, eto ung format nung mga marereturn or makukuhang data.


"""
import datetime
from typing import Optional, Annotated, Union
from pydantic import BaseModel
from fastapi import Query


class Token(BaseModel):
    access_token: str 
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


# class Login(BaseModel):
	
class UserPlantsResponse(BaseModel):
	user_id: int = None
	plant_id: int = None
	is_harvested: bool = None
	date_planted: datetime.date = None
	min_date_estimate_harvest: datetime.date = None
	max_date_estimate_harvest: datetime.date = None
	date_harvested: Optional[datetime.date] = None


class FilterCurrentUserPlants(BaseModel):
	category: Optional[str] = None
	is_harvested: Optional[bool] = None

	
class CurrentUserPlants(BaseModel):
	name: str = None
	category: str = None
	is_harvested: bool = None
	date_planted: datetime.date = None
	min_date_estimate_harvest: datetime.date = None
	max_date_estimate_harvest: datetime.date = None
	date_harvested: Optional[datetime.date] = None


class PlantsResponse(BaseModel):
	id: int = None
	name: str = None
	category: str = None
	p_info: str = None 
	min_temp: float = None
	max_temp: float = None
	min_humidity: float = None
	max_humidity: float = None
	min_rain_tolerance: float = None
	max_rain_tolerance: float = None
	min_planting_time: int = None
	max_planting_time: int = None
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
	min_rain_tolerance: float = None
	max_rain_tolerance: float = None 
	min_planting_time: int = None
	max_planting_time: int = None
	summer: bool = None
	rainy_season: bool = None

# class UserPlantsRequest(BaseModel):

# class CurrentUserPlants(BaseModel):
# 	plants: list[PlantsResponse]

# 	class Config:
# 		orm_mode = True	

class Login(BaseModel):
	username: str = None
	password: str = None

class SignUpRequest(BaseModel):
	username: str = None
	# birthday: Optional[datetime.date] = None
	pass_to_hash: str = None
	country: str = None
	state: str = None
	city: str = None
	is_active: bool = False
	is_public: bool = True

class SignUpResponse(BaseModel):
	id: int
	username: str = None
	# birthday: Optional[datetime.date] = None
	# hashed_pass: str = None
	country: str = None
	state: str = None
	city: str = None
	is_active: bool= False
	is_public: bool = True

	class Config:
		orm_mode = True

# same for update
class UserResponse(BaseModel):
	id: int
	username: str = None
	firstname: Optional[str] = None
	lastname: Optional[str] = None
	birthday: Optional[datetime.date] = None
	# hashed_pass: str = None
	country: str = None
	state: str = None
	city: str = None
	is_active: bool= False
	is_public: bool = True
	plants: list[UserPlantsResponse] = []

	class Config:
		orm_mode = True	


class UserFilterRequest(BaseModel):
	upperAge: Optional[int] = None 
	lowerAge: Optional[int] = None
	country: Optional[str] = None
	state: Optional[str] = None
	city: Optional[str] = None
	is_active: Optional[bool] = None
	is_public: Optional[bool] = None

class UserUpdateRequest(BaseModel):
	firstname: str = None
	lastname: str = None
	birthday: datetime.date = None
	country: str = None
	state: str = None
	city: str = None
	is_public: bool = False


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
	min_rain_tolerance: float = None
	max_rain_tolerance: float = None
	min_planting_time: int = None
	max_planting_time: int = None
	summer: bool = None
	rainy_season: bool = None

class PlantFilterRequest(BaseModel):
	name: Optional[str] = None
	category: Optional[str] = None
	upper_p_time: Optional[int] = None
	lower_p_time: Optional[int] = None
	summer: Optional[bool] = None
	rainy_season: Optional[bool] = None


class UserPlantsRequest(BaseModel):
	is_harvested: bool = False
	date_planted: datetime.date = None

class UserPlantUpdate(BaseModel):
	is_harvested: bool = True
	date_harvested: datetime.date = None


class UserPlantsFilter(BaseModel):
	is_harvested: Optional[bool] = None


# <<<<<<< HEAD
# =======
# 	rainy_season: Optional[bool] = None
# >>>>>>> origin/ciavel
