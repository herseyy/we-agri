from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError

from .models import UserPlants, User, Plant
from .schemas import UserRequest, UserResponse, PlantRequest, UserFilterRequest, UserUpdateRequest, UserChangePass

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

def filter_users(db:Session, user_filter: UserFilterRequest = None, q: int = None):
	query = db.query(User)

	if user_filter == None:
		return query.all()

	if q is not None:
		plants_ = []
		ids = []
		qry = db.query(UserPlants).join(User)
		for i in query.all():
			qry = qry.filter(UserPlants.user_id == i.id)

			for j in qry:
				plants_.append(j.plant_id)

			# print(plants_)
			# print(q)
			new_list=  all(item in plants_ for item in q)
			if new_list is True:
				ids.append(i.id)
				# print(i.id) 
			qry = db.query(UserPlants).join(User)
			plants_ = []

		if ids != []:
			query = query.filter(or_(User.id == x for x in ids))
		else:
			query = query.filter(User.id == 0)


	if user_filter.upperAge is not None and user_filter.lowerAge is not None:
		lower_day = datetime.now() - relativedelta(years = user_filter.upperAge + 1)
		# print(lower_day)
		upper_day = datetime.now() - relativedelta(years = user_filter.lowerAge)
		# print(upper_day)

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
	# if user_filter.plants is not None:
		# query = query.filter()

	return query.all()


def change_pass(db: Session, id: int, pass_: UserChangePass):
	current_user = db.query(User).filter(User.id == id).first()

	status = {
		"status": "success"
	}

	if current_user is None:
		status["status"] = "user not found!"
		return status
	if pass_.old_pass is not None and pass_.old_pass == current_user.hashed_pass:
		if pass_.old_pass == pass_.new_pass1:
			status["status"] = "error new pass can't be the same as old"
			return status
		elif pass_.new_pass1 is not None and pass_.new_pass2 == pass_.new_pass1:
			current_user.hashed_pass = pass_.new_pass1
		else:
			status["status"] = "pass1 != pass2"
			return status
	else:
		status["status"] = "incorrect old pass"
		return status

	db.commit()

	return status

# def get_user_plants(db: Session, id: int):
# 	current_plants = db.query(UserPlants).filter(UserPlants.user_id == id).all()

# 	# for key, value in current_plants.items() :
# 	# 	print (key, value)

# 	return current_plants


def update_user(db: Session, id: int, info: UserUpdateRequest):

	current_user = db.query(User).filter(User.id == id).first()

	if current_user is None:
		return current_user

	if info.birthday != current_user.birthday:
		current_user.birthday = info.birthday
	if info.province != current_user.province:
		current_user.province = info.province
	if info.city != current_user.city:
		current_user.city = info.city
	if info.is_public != current_user.is_public:
		current_user.is_public = info.is_public

	db.commit()

	return current_user



def format_user(db_user: User):
    _plants = []

    plants = db_user.plants
    # print(plants)
# 
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
            rainy_season = plant.rainy_season
			)
		db.add(db_plant)
     	db.commit()
	
    except IntegrityError:
     	db.rollback()
		raise HTTPException(status_code=401, detail="Some fields have constraints!")
    
    return db_plant