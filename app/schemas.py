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


# class UserUpdateRequest(BaseModel):
# 	birthday:
	


# 	username: str = None
# 	birthday: Optional[datetime.date] = None
# 	hashed_pass1: str = None
# 	hashed_pass2: str = None
# 	province: str = None
# 	city: str = None
# 	is_active: bool = False
# 	is_public: bool = True
# 	plants: list[int]


# 	    date_positive: datetime.date = None
#     age: int = None
#     months: int = None
#     days: int = None
#     # birthday: datetime.date
#     sex: str = None
#     barangay: str = None
#     contact_number: str = None
#     asymptomatic: bool = True
#     status: str = None