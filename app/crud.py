from fastapi import HTTPException, Depends, status, Request

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError

from .models import UserPlants, User, Plant
from .schemas import SignUpRequest, SignUpResponse, UserResponse, PlantRequest, PlantsResponse, UserFilterRequest, UserUpdateRequest, UserChangePass, CurrentUserPlants, PlantUpdate, PlantFilterRequest, Token, TokenData, UserPlantsRequest, UserPlantUpdate, UserPlantsResponse, FilterCurrentUserPlants, Login
# from .server import get_db

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  


# SECRET_KEY = "4882fb01f85938a7b77a1cc157c84a4b3cee06e069ce6bc880235755f190de18"
# ALGORITHM = "HS256"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def get_db(request: Request):
#     return request.state.db


# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)




# # di pa tapos
# def get_user_by_username(db:Session, username_: str):
# 	user = db.query(User).filter(User.username == username_).first()

# 	if user:
# 		return user


# def authenticate_user(db:Session, username: str, password: str):
#     user = get_user_by_username(db, username)
#     # print(user)
#     if not user: 
#         return False
#     if not verify_password(password, user.hashed_pass):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta or None = None): 
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else: 
#         expire = datetime.utcnow() + timedelta(minutes=15)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user_(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
#     credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
#     try :
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None: 
#             raise credential_exception
        
#         token_data = TokenData(username=username)
        
#     except JWTError:
#         raise credential_exception

#     user = get_user_by_username(db, username_=token_data.username) 
#     if user is None: 
#         raise credential_exception
    
#     return user


# async def get_current_active_user(current_user: UserRequest = Depends(get_current_user)):
# 	# print(current_user.is_active)
# 	if not current_user.is_active:
# 	    raise HTTPException(status_code=400, detail= "Inactive user")

# 	return current_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_hash_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

# get user from token
def decode(token, SECRET_KEY, ALGORITHM, db):
    # try:
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    username = payload.get('sub')

    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(404, detail="User not found!")

    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    return user





def create_user(db:Session, user: SignUpRequest):
	try:
		user_n = db.query(User).filter(User.username == user.username).first()
		if user_n:
			# print('hehe')
			return None

		hashed_pass = get_hash_password(user.pass_to_hash)

		db_user = User(
			username = user.username,
			# birthday = user.birthday,
			hashed_pass = hashed_pass,
			country = user.country,
			state = user.state,
			city = user.city,
			is_public = user.is_public
			)
		db.add(db_user)
		# db.flush()

		# for i in user.plants:
		# 	db_plants = UserPlants(
		# 		user_id = db_user.id,
		# 		plant_id = i
		# 		)
		# 	db.add(db_plants)
		# db.flush()
		db.commit()

	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=401, detail="Some fields have constraints!")

	return db_user

def filter_users(db:Session, user_filter: UserFilterRequest = None, q: int = None):

	query = db.query(User)

	# print(query)
	if user_filter == None:
		print('a')
		return query.all()

	if q is not None:
		plants_ = []
		ids = []
		qry = db.query(UserPlants).join(User)
		for i in query.all():
			if 0 in q:
				qry1 = qry.filter(UserPlants.user_id != i.id)
				for l in qry1:
					ids.append(i.id)
			else:
				qry = qry.filter(UserPlants.user_id == i.id)
				# print(i.id)
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
	if user_filter.country is not None:
		query = query.filter(User.country == user_filter.country)
	if user_filter.state is not None:
		query = query.filter(User.state == user_filter.state)
	if user_filter.city is not None:
		query = query.filter(User.city == user_filter.city)
	if user_filter.is_active is not None:
		query = query.filter(User.is_active == user_filter.is_active)
	if user_filter.is_public is not None:
		query = query.filter(User.is_public == user_filter.is_public)
	# if user_filter.plants is not None:
		# query = query.filter()

	return query.all()


def change_pass(db: Session, current_user: User, pass_: UserChangePass):
	# current_user = db.query(User).filter(User.id == id).first()

	status = {
		"status": "success"
	}

	if pass_.old_pass is not None and verify_password(pass_.old_pass, current_user.hashed_pass):
		if pass_.old_pass == pass_.new_pass1:
			status["status"] = "error new pass can't be the same as old"
			print("Error old pass == new pass")
			return status
		elif pass_.new_pass1 == "":
			status["status"] = "Enter new pass"
			print("Enter new pass")
			return status
		elif len(pass_.new_pass1) < 5:
			status["status"] = "pass too short"
			print("pass too short")
			return status
		elif pass_.new_pass1 != "" and pass_.new_pass2 == pass_.new_pass1:
			current_user.hashed_pass = get_hash_password(pass_.new_pass1)
		else:
			status["status"] = "pass1 != pass2"
			print("pass!=pass1")
			return status
	else:
		status["status"] = "incorrect old pass"
		print("incorrect old pass_")
		return status
	db.commit()

	return status

def get_current_user(db: Session, id: int):
	current_user = db.query(User).filter(User.id == id).first()

	return current_user

# def get_all_user_plants(db: Session):
# 	all_user_plants = db.query(UserPlants).all()

# 	plants = []

# 	for i in all_user_plants:
# 		plants.append(i.description)

# 	return plants

# def get_user_plants(db: Session, user_plants: list):
# 	# user_plants = db.query(UserPlants).filter(UserPlants.user_id == id).all()
# 	print(user_plants)
# 	plants = []
# 	for i in user_plants:
# 		# print(i.description)
# 		plants.append(i.description)
# 	# print(plants)
# 	return plants


def delete_user_plant(db: Session, user_id: int, plant_id: int):
	plant = db.query(UserPlants)\
	.filter(UserPlants.user_id == user_id)\
	.filter(UserPlants.plant_id == plant_id).delete()

	db.commit()

	remaining_plants = db.query(UserPlants).filter(UserPlants.user_id == user_id).all()

	# remaining_plants_lst = []
	# for i in remaining_plants:
	# 	# print(i.description)
	# 	remaining_plants_lst.append(i.description)
	# # print(plants)
	return remaining_plants


def add_user_plant(db: Session, plant_info:UserPlantsRequest, current_user: User, plant_id:int):

	# current_user = db.query(User).filter(User.id == user_id).first()

	# if current_user is None:
	# 	return False

	# print(plant_info.is_harvested)
	# print(plant_info.date_planted) # 2023-05-16

	plant = db.query(Plant).filter(Plant.id == plant_id).first()

	# print(plant.min_planting_time) # 3
	# print(plant.max_planting_time) # 5
	min_planting_time_in_days = plant.min_planting_time * 7
	max_planting_time_in_days = plant.max_planting_time * 7

	min_date_plant = plant_info.date_planted + timedelta(days=min_planting_time_in_days)
	max_date_plant = plant_info.date_planted + timedelta(days=max_planting_time_in_days)

	print(min_date_plant)
	print(max_date_plant)

	today = date.today()
	if today > max_date_plant:
		is_harvested = True
	else:
		is_harvested = False
	# to check if yung user is may plant na na yun
	plants_old = db.query(UserPlants).filter(UserPlants.user_id == current_user.id).all()
	# print(plants_old)
	for i in plants_old:
		if plant_id == i.plant_id:
			return None
	if is_harvested == True:
		db_plants = UserPlants(
			user_id = current_user.id,
			plant_id = plant_id,
			is_harvested = is_harvested,
			date_planted = plant_info.date_planted,
			min_date_estimate_harvest = min_date_plant,
			max_date_estimate_harvest = max_date_plant,
			date_harvested = max_date_plant
		)
	else:
		db_plants = UserPlants(
			user_id = current_user.id,
			plant_id = plant_id,
			is_harvested = is_harvested,
			date_planted = plant_info.date_planted,
			min_date_estimate_harvest = min_date_plant,
			max_date_estimate_harvest = max_date_plant,
		)
	db.add(db_plants)
	db.commit()

	plants_new = db.query(UserPlants).filter(UserPlants.user_id == current_user.id).all()
	# print(plant_)

	plants_1 = []
	for i in plants_new:
		# print(i.description)
		plants_1.append(i.description)

	return plants_1


def update_user_plant(db: Session, plant_info:UserPlantsRequest, current_user: User, plant_id:int):

	user_plant = db.query(UserPlants).filter(UserPlants.user_id == current_user.id)\
				.filter(UserPlants.plant_id == plant_id).first()
	# print(user_plant)


	if plant_info.is_harvested != None:
		user_plant.is_harvested = plant_info.is_harvested
	if plant_info.date_harvested != None:
		user_plant.date_harvested = plant_info.date_harvested

	db.commit()
	updated_user_plant = db.query(UserPlants).filter(UserPlants.user_id == current_user.id)\
				.filter(UserPlants.plant_id == plant_id).first()

	return updated_user_plant


def filter_user_plants(user: User, db:Session, user_plant_filter: FilterCurrentUserPlants = None):
	query = db.query(UserPlants).filter(UserPlants.user_id == user.id)

	# print(user_plant_filter.category)
	if user_plant_filter.is_harvested != None:
		query = query.filter(UserPlants.is_harvested == user_plant_filter.is_harvested)
	if user_plant_filter.category != None:
		query = query.filter(UserPlants.category.value == user_plant_filter.category)
	return query.all()

def format_plants(db_plant: Plant):
	# print(db_plant)
	if db_plant is None:
		# print('aaa')
		return []
	return PlantsResponse(
		id = db_plant.id,
		name = db_plant.name,
		category = db_plant.category.value,
		p_info = db_plant.p_info,
		min_temp = db_plant.min_temp,
		max_temp = db_plant.max_temp,
		min_humidity = db_plant.min_humidity,
		max_humidity = db_plant.max_humidity,
		min_rain_tolerance = db_plant.min_rain_tolerance,
		max_rain_tolerance = db_plant.max_rain_tolerance,
		min_planting_time = db_plant.min_planting_time,
		max_planting_time = db_plant.max_planting_time,
		summer = db_plant.summer,
		rainy_season = db_plant.rainy_season,
	    )

def format_user_plants(db_user_plants: UserPlants):
	if db_user_plants is None:
		# print('aaa')
		return []
	# print(db_user_plants)
	return UserPlantsResponse(
		user_id = db_user_plants.user_id,
		plant_id = db_user_plants.plant_id,
		is_harvested = db_user_plants.is_harvested,
		date_planted = db_user_plants.date_planted,
		min_date_estimate_harvest = db_user_plants.min_date_estimate_harvest,
		max_date_estimate_harvest = db_user_plants.max_date_estimate_harvest,
		date_harvested = db_user_plants.date_harvested
		)


def update_user(db: Session, current_user: User, info: UserUpdateRequest):

	# current_user = db.query(User).filter(User.username == username).first()

	# if current_user is None:
		# return current_user
	if info.firstname != current_user.firstname:
		current_user.firstname = info.firstname
	if info.lastname != current_user.lastname:
		current_user.lastname = info.lastname
	if info.birthday != current_user.birthday:
		current_user.birthday = info.birthday
	if info.state != current_user.state:
		current_user.state = info.state
	if info.country != current_user.country:
		current_user.country = info.country
	if info.city != current_user.city:
		current_user.city = info.city
	if info.is_public != current_user.is_public:
		current_user.is_public = info.is_public

	db.commit()

	return current_user


def delete_user(db:Session, user_id: int, pass_: str):

	user_d = db.query(User).filter(User.id == user_id).first()

	
	if pass_ is not None and verify_password(pass_, user_d.hashed_pass):
		print(True)
	else:
		return {"fail": "incorrect pass"}

	db.query(User).filter(User.id == user_id).delete()

	db.query(UserPlants).filter(UserPlants.user_id == user_id).delete()

	db.commit()

	return {"success": "ok"}



def format_user(db_user: User):
	# print(db_user.plants)
	_plants = []

	# if db_user.plants is None:
	# 	print('a')

	plants = db_user.plants
	# for i in plants:
	#     if plants is not None:
	#     	_plants.append(i.description)


	    # format_user_plants

	return UserResponse(
		id = db_user.id,
		username = db_user.username,
		firstname = db_user.firstname,
		lastname = db_user.lastname,
		birthday = db_user.birthday,
		# hashed_pass = db_user.hashed_pass,
		country = db_user.country,
		state = db_user.state,
		city = db_user.city,
		is_active = db_user.is_active,
		is_public = db_user.is_public,
		plants = [format_user_plants(plant) for plant in plants]
	    )


def create_plant(db:Session, plant: PlantRequest):
    try:
     	db_plant = Plant(
			name = plant.name.lower(),
			category = plant.category,
			p_info = plant.p_info,
			min_temp = plant.min_temp,
            max_temp = plant.max_temp,
            min_humidity = plant.min_humidity,
            max_humidity = plant.max_humidity,
            min_rain_tolerance = plant.min_rain_tolerance,
            max_rain_tolerance = plant.max_rain_tolerance,
            min_planting_time = plant.min_planting_time,
            max_planting_time = plant.max_planting_time,
            summer = plant.summer,
            rainy_season = plant.rainy_season,
			)
     	db.add(db_plant)
     	db.commit()
    except IntegrityError:
     	db.rollback()
     	raise HTTPException(status_code=401, detail="Some fields have constraints!")
    return db_plant


def filter_plants(db: Session, plant_filter: PlantFilterRequest = None):
	query = db.query(Plant)
	# print(plant_filter.name.lower())
	if plant_filter.name is not None:
		query = query.filter(Plant.name == plant_filter.name.lower())
	if plant_filter.category is not None:
		query = query.filter(Plant.category == plant_filter.category)



	if plant_filter.upper_p_time is not None and plant_filter.lower_p_time is not None:
		query = query.filter(
					and_((Plant.planting_time >=  plant_filter.lower_p_time),
						(Plant.planting_time <= plant_filter.upper_p_time)))


		
	if plant_filter.summer is not None:
		query = query.filter(Plant.summer == plant_filter.summer)
	if plant_filter.rainy_season is not None:
		query = query.filter(Plant.rainy_season == plant_filter.rainy_season)

	return query.all()


def update_plant(db: Session, plant_id: int, info: PlantUpdate):
	plant = db.query(Plant).filter(Plant.id == plant_id).first()

	if plant is None:
		return plant

	if info.name != plant.name:
		plant.name = info.name
	if info.category != plant.category:
		plant.category = info.category
	if info.p_info != plant.p_info:
		plant.p_info = info.p_info
	if info.min_temp != plant.min_temp:
		plant.min_temp = info.min_temp
	if info.max_temp != plant.max_temp:
		plant.max_temp = info.max_temp
	if info.min_humidity != plant.min_humidity:
		plant.min_humidity = info.min_humidity
	if info.max_humidity != plant.max_humidity:
		plant.max_humidity = info.max_humidity
	if info.min_rain_tolerance != plant.min_rain_tolerance:
		plant.max_rain_tolerance = info.max_rain_tolerance
	if info.min_planting_time != plant.min_planting_time:
		plant.min_planting_time = info.min_planting_time
	if info.max_planting_time != plant.max_planting_time:
		plant.max_planting_time = info.max_planting_time
	if info.summer != plant.summer:
		plant.summer = info.summer
	if info.rainy_season != plant.rainy_season:
		plant.rainy_season = info.rainy_season

	db.commit()

	return plant




def delete_plant(db: Session, plant_id: int):
	plant_d = db.query(Plant).filter(Plant.id == plant_id).delete()
	user_plant_d = db.query(UserPlants).filter(UserPlants.plant_id == plant_id).delete()
	# print(user_plant_d)

	db.commit()

	remaining_plants = db.query(Plant).all()

	return remaining_plants



# def add_img_to_db(db:Session, pla)





# def get_current_user_plants(user:User, db: Session):
# 	my_plants = db.query(UserPlants).filter(UserPlants.user_id == user.id).all()
# 	lst = []
# 	for i in my_plants:
# 		plant_description = db.query(Plant).filter(Plant.id == i.plant_id).first()
# 		plant_join = CurrentUserPlants(
# 			name = plant_description.name,
# 			category = plant_description.category.value,
# 			is_harvested = i.is_harvested,
# 			date_planted = i.date_planted,
# 			min_date_estimate_harvest = i.min_date_estimate_harvest,
# 			max_date_estimate_harvest = i.max_date_estimate_harvest,
# 			date_harvested = i.date_harvested
# 			)
# 		lst.append(plant_join)
# 	return lst

def get_current_user_plants_filter(user:User, db: Session, filter_plants: FilterCurrentUserPlants):
	my_plants = db.query(UserPlants).filter(UserPlants.user_id == user.id)

	if filter_plants.category != None:
		fil_cat = db.query(Plant).filter(Plant.category == filter_plants.category).all()
		id_cat = []
		for j in fil_cat:
			id_cat.append(j.id)
		print(id_cat)
		my_plants = db.query(UserPlants).filter(UserPlants.plant_id.in_(id_cat))
		# db_session.query(Star).filter(Star.star_type.in_(['Nova', 'Planet']))

	if filter_plants.is_harvested != None:
		my_plants = my_plants.filter(UserPlants.is_harvested == filter_plants.is_harvested)

	lst = []
	for i in my_plants:
		plant_description = db.query(Plant).filter(Plant.id == i.plant_id).first()

		# if filter_plants.category != None:
		# 	plant_description = plant_description.filter()

		plant_join = CurrentUserPlants(
			id = plant_description.id,
			name = plant_description.name,
			category = plant_description.category.value,
			is_harvested = i.is_harvested,
			date_planted = i.date_planted,
			min_date_estimate_harvest = i.min_date_estimate_harvest,
			max_date_estimate_harvest = i.max_date_estimate_harvest,
			date_harvested = i.date_harvested
			)
		lst.append(plant_join)
	return lst

