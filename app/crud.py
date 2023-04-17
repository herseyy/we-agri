from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from .models import UserPlants, User, Plant
from .schemas import UserRequest, UserResponse


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



def format_user(db_user: User):
    _plants = []

    plants = db_user.plants
    print(plants)

    for i in plants:
        if plants is not None:
            _plants.append(i.description)

    return UserResponse(
		id = db_user.id,
		username = db_user.username,
		birthday = db_user.birthday,
		hashed_pass = db_user.hashed_pass,
		province = db_user.province,
		city = db_user.city,
		is_active = db_user.is_active,
		is_public = db_user.is_public,
		plants = _plants
        )

