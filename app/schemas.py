"""
Schema file

Ang ibig sabihin lang neto, eto ung format nung mga marereturn or makukuhang data.


"""
import datetime
from typing import Optional
from pydantic import BaseModel

class PlantsResponse(BaseModel):
	id: int
	name: str = None
	min_temp: int = None
	max_temp: int = None
	min_humidity: int = None
	max_humidity: int = None
	rain_tolerance: int = None
	planting_time: int = None
	summer: bool = False
	rainy_season: bool = False

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
	plants: list[int]


class PlantRequest(BaseModel):
	name: str = None     
	p_info: str = None 
	min_temp: float = None
	max_temp: float = None
	min_humidity: float = None
	max_humidity: float = None
	rain_tolerance: float = None 
	planting_time: int = None
	summer: bool = None
	rainy_season: bool = None



# same for update
class UserResponse(BaseModel):
	id: int
	username: str = None
	birthday: Optional[datetime.date] = None
	hashed_pass: str = None
	province: str = None
	city: str = None
	is_active: bool= False
	is_public: bool = True
	plants: list[PlantsResponse]

	class Config:
		orm_mode = True	


class UserUpdateRequest(BaseModel):
	birthday: Optional[datetime.date] = None
	province: str = None
	city: str = None
	is_public: bool= True
	plants: list[int]



