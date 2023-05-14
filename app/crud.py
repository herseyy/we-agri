from fastapi import HTTPException, Depends, status, Request

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError

from .models import UserPlants, User, Plant
from .schemas import UserRequest, UserResponse, PlantRequest, PlantsResponse, UserFilterRequest, UserUpdateRequest, UserChangePass, CurrentUserPlants, PlantUpdate, PlantFilterRequest, Token, TokenData
# from .server import get_db

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt  


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









def create_user(db:Session, user: UserRequest):
	try:
		user_n = db.query(User).filter(User.username == user.username).first()
		if user_n:
			# print('hehe')
			return None
		hashed_pass = get_password_hash(user.pass_to_hash1)

		db_user = User(
			username = user.username,
			birthday = user.birthday,
			hashed_pass = hashed_pass,
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

	print(user_filter)
	if user_filter == None:
		print('a')
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
	# print(get_password_hash("pass"))
	# print(current_user.hashed_pass)


	# if verify_password(pass_.old_pass, current_user.hashed_pass):
	# 	print(True)

	if current_user is None:
		return current_user
	if pass_.old_pass is not None and verify_password(pass_.old_pass, current_user.hashed_pass):
		if pass_.old_pass == pass_.new_pass1:
			status["status"] = "error new pass can't be the same as old"
			return status
		elif pass_.new_pass1 is not None and pass_.new_pass2 == pass_.new_pass1:
			current_user.hashed_pass = get_password_hash(pass_.new_pass1)
		else:
			status["status"] = "pass1 != pass2"
			return status
	else:
		status["status"] = "incorrect old pass"
		return status
	# print(current_user.hashed_pass)
	# if verify_password(pass_.new_pass1, current_user.hashed_pass):
	# 	print(True)

	db.commit()

	return status

def get_current_user(db: Session, id: int):
	current_user = db.query(User).filter(User.id == id).first()

	return current_user

def get_all_user_plants(db: Session):
	all_user_plants = db.query(UserPlants).all()

	plants = []

	for i in all_user_plants:
		plants.append(i.description)

	return plants

def get_user_plants(db: Session, user_plants: list):
	# user_plants = db.query(UserPlants).filter(UserPlants.user_id == id).all()
	# print(user_plants)
	plants = []
	for i in user_plants:
		# print(i.description)
		plants.append(i.description)
	# print(plants)
	return plants


def delete_user_plant(db: Session, user_id: int, plant_id: int):
	plant = db.query(UserPlants)\
	.filter(UserPlants.user_id == user_id)\
	.filter(UserPlants.plant_id == plant_id).delete()

	db.commit()

	remaining_plants = db.query(UserPlants).filter(UserPlants.user_id == user_id).all()

	remaining_plants_lst = []
	for i in remaining_plants:
		# print(i.description)
		remaining_plants_lst.append(i.description)
	# print(plants)
	return remaining_plants_lst


def add_user_plant(db: Session, user_id: int, plant_id:int):

	current_user = db.query(User).filter(User.id == user_id).first()

	if current_user is None:
		return False

	plants_old = db.query(UserPlants).filter(UserPlants.user_id == user_id).all()
	# print(plants_old)
	for i in plants_old:
		if plant_id == i.plant_id:
			return None

	db_plants = UserPlants(
		user_id = user_id,
		plant_id = plant_id
		)
	db.add(db_plants)
	db.commit()

	plants_new = db.query(UserPlants).filter(UserPlants.user_id == user_id).all()
	# print(plant_)

	plants_1 = []
	for i in plants_new:
		# print(i.description)
		plants_1.append(i.description)

	return plants_1

def format_plants(db_plant: Plant):
	# print(db_plant.id)
	return PlantsResponse(
		id = db_plant.id,
		name = db_plant.name,
		category = db_plant.category.value,
		p_info = db_plant.p_info,
		min_temp = db_plant.min_temp,
		max_temp = db_plant.max_temp,
		min_humidity = db_plant.min_humidity,
		max_humidity = db_plant.max_humidity,
		rain_tolerance = db_plant.rain_tolerance,
		planting_time = db_plant.planting_time,
		summer = db_plant.summer,
		rainy_season = db_plant.rainy_season,
	    )


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


def delete_user(db:Session, user_id: int):
	user_d = db.query(User).filter(User.id == user_id).delete()

	user_d_plants = db.query(UserPlants).filter(UserPlants.user_id == user_id).delete()

	db.commit()

	remaining_users = db.query(User).all()

	return remaining_users


def format_user(db_user: User):
	# print(db_user)
	_plants = []

	plants = db_user.plants

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
		plants = [format_plants(plant) for plant in _plants]
	    )


def create_plant(db:Session, plant: PlantRequest):
    try:
     	db_plant = Plant(
			name = plant.name,
			category = plant.category,
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


def filter_plants(db: Session, plant_filter: PlantFilterRequest = None):
	query = db.query(Plant)


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
	if info.rain_tolerance != plant.rain_tolerance:
		plant.rain_tolerance = info.rain_tolerance
	if info.planting_time != plant.planting_time:
		plant.planting_time = info.planting_time
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











