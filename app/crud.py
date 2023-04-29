from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from .models import UserPlants, User, Plant
from .schemas import UserRequest, UserResponse, PlantRequest, UserFilterRequest

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta



def create_user(db:Session, user: UserRequest):

	try:
		print(user.hashed_pass1)
		print(user.hashed_pass2)

		db_user = User(
			username = user.username,
			birthday = user.birthday,
			hashed_pass = user.hashed_pass1,
			province = user.province,
			city = user.city,
			is_public = user.is_public
			)
		db.add(db_user)
		db.flush()

		for i in user.plants:
			db_plants = UserPlants(
				user_id = db_user.id,
				plant_id = i
				)
			db.add(db_plants)
		db.flush()
		db.commit()

	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=401, detail="Some fields have constraints!")

	return db_user

def filter_users(db:Session, user_filter: UserFilterRequest = None):
	query = db.query(User)

	if user_filter == None:
		return query.all()
	if user_filter.upperAge is not None and user_filter.lowerAge is not None:
		lower_day = datetime.now() - relativedelta(years = user_filter.upperAge + 1)
		print(lower_day)
		upper_day = datetime.now() - relativedelta(years = user_filter.lowerAge)
		print(upper_day)

		query = query.filter(
            and_((User.birthday >= lower_day), 
            (User.birthday <= upper_day)))
	if user_filter.province is not None:
		query = query.filter(User.province == user_filter.province)
	if user_filter.city is not None:
		query = query.filter(User.city == user_filter.city)
	if user_filter.is_active is not None:
		query = query.filter(User.is_active == user_filter.is_active)
	if user_filter.is_public is not None:
		query = query.filter(User.is_public == user_filter.is_public)

	return query.all()

# def update_users(db)













def update_user(db: Session, id: int):

	current_user = db.query(User).filter(User.id == id).first()

	
	# plants: list[int]


	# if info.birthday != current_user.birthday:
	# 	current_user.birthday = info.birthday
	# if info.province != current_user.province:
	# 	current_user.province = info.province
	# if info.city != current_user.city:
	# 	current_user.city = info.city
	# if info.is_public != current_user.is_public:
	# 	current_user.is_public = info.is_public
	# if 
	


	return current_user



def format_user(db_user: User):
    _plants = []

    plants = db_user.plants
    print(db_user)

    for i in plants:
        if plants is not None:
            _plants.append(i.description)

    return UserResponse(
		id = db_user.id,
		username = db_user.username,
		birthday = db_user.birthday,
		# hashed_pass = db_user.hashed_pass,
		province = db_user.province,
		city = db_user.city,
		is_active = db_user.is_active,
		is_public = db_user.is_public,
		plants = _plants
        )











def create_plant(db:Session, plant: PlantRequest):
     
    try:
     	db_plant = Plant(
			name = plant.name,
			p_info = plant.p_info,
			min_temp = plant.min_temp,
            max_temp = plant.max_temp,
            min_humidity = plant.min_humidity,
            max_humidity = plant.max_humidity,
            rain_tolerance = plant.rain_tolerance,
            planting_time = plant.planting_time,
            summer = plant.summer,
            rainy_season = plant.rainy_season,
			)
     	db.add(db_plant)
     	db.commit()
    except IntegrityError:
     	db.rollback()
     	raise HTTPException(status_code=401, detail="Some fields have constraints!")
    return db_plant
