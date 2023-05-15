"""
Main file
"""
from fastapi import FastAPI, Request, Response, Depends, HTTPException, Query, status
from typing import Optional, Annotated, Union
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# from fastapi.templating import Jinja2Templates

from . import crud, models, schemas, owm, login
from .database import SessionLocal, engine




# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta







# Matic nagccreate na ng table
models.Base.metadata.create_all(bind=engine)


# SECRET_KEY = "4882fb01f85938a7b77a1cc157c84a4b3cee06e069ce6bc880235755f190de18"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Main app object
app = FastAPI()


origins = [
    "http://localhost.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Wag mo muna tong pansinin, malilito ka lang
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Db dependency, get db
def get_db(request: Request):
    return request.state.db


def populate_table():
    db = SessionLocal()
    # crud.populate_diseases(db)
    db.close()


populate_table()

@app.get("/")
def index():
    return {"Hello": "World"}



# @app.post("/token", response_model=schemas.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
#     user = crud.authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = crud.create_access_token(
#         data= {"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me/", response_model=schemas.UserResponse)
# async def read_users_me(current_user : schemas.UserRequest = Depends(crud.get_current_user_)):
#     return current_user

# @app.get("/users/me/items/")
# async def read_own_items(current_user : schemas.UserRequest = Depends(crud.get_current_user_)):
#     return [{"item_id": 1, "owner": current_user}]





##### USERS

# , response_model = schemas.UserResponse
@app.post("/create_user", response_model = schemas.UserResponse)
def create_user(user: schemas.UserRequest, db:Session = Depends(get_db)):
    created_user = crud.create_user(db=db, user=user)
    # print(created_user)
    if created_user == None:
        raise HTTPException(404, detail="Username is already taken")
        # return {"message": "username is taken"}


    return crud.format_user(created_user)

@app.get("/filter_users", response_model = list[schemas.UserResponse])
def filter_users(user_filter: schemas.UserFilterRequest = Depends(), q: Union[list[int], None] = Query(default=None), db:Session = Depends(get_db)):
    users = crud.filter_users(db, user_filter, q)
    # for user in users:    
    #     print(crud.format_user(user))
    return [crud.format_user(user) for user in users]





  
@app.patch("/update_user/{user_id}")
def update_user(user_id: int, info: schemas.UserUpdateRequest, db: Session = Depends(get_db), token:str=Depends(login.oauth2_scheme)):
    current_user = crud.update_user(db=db, id=user_id, info=info)

    if current_user is None:
        raise HTTPException(404, detail="User not found!")

    return crud.format_user(current_user)






@app.patch("/change_pass/{user_id}")
def change_pass(user_id: int, pass_:schemas.UserChangePass, db:Session = Depends(get_db)):
    current_user = crud.change_pass(db=db, id=user_id, pass_=pass_)

    if current_user is None:
        raise HTTPException(404, detail="User not found!")

    return current_user


@app.get("/get_all_user_plants")
def get_all_user_plants(db: Session = Depends(get_db)):
    user_plants = db.query(models.UserPlants).all()

    plants = crud.get_user_plants(db=db, user_plants = user_plants)

    print(user_plants)
    return [crud.format_plants(plant) for plant in plants]

@app.get("/get_user_plants/{user_id}")
def get_user_plants(user_id: int, db:Session = Depends(get_db)):

    user_plants = db.query(models.UserPlants).filter(models.UserPlants.user_id == user_id).all()
    plants = crud.get_user_plants(db=db, user_plants=user_plants)

    message = {
        "message": "user no plants"
    }

    if plants is None or plants == []:
        return message
        # raise HTTPException(404, detail="No plant found!")

    return [crud.format_plants(plant) for plant in plants]


@app.delete("/delete_user_plant/{user_id}/{plant_id}")
def delete_user_plant(user_id: int, plant_id: int, db:Session = Depends(get_db)):
    plants = crud.delete_user_plant(db=db, user_id= user_id, plant_id= plant_id)

    message = {
        "message": "user no plants"
    }

    if plants is None or plants == []:
        return message

    return [crud.format_plants(plant) for plant in plants]


@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    users = crud.delete_user(db = db, user_id = user_id)


    return [crud.format_user(user) for user in users]

@app.post("/add_user_plant/{user_id}/{plant_id}")
def add_user_plant(user_id: int, plant_id: int, db:Session = Depends(get_db)):
    plants = crud.add_user_plant(db=db, user_id= user_id, plant_id= plant_id)

    message = {
        "message": "user already has this plant"
    }

    if plants is False:
        return {"message": "No user found"}

    if plants is None or plants == []:
        return message

    return [crud.format_plants(plant) for plant in plants]


    

##### PLANTS

@app.post("/create_plant", response_model = schemas.PlantsResponse)
def create_plant(plant: schemas.PlantRequest, db:Session = Depends(get_db)):
    created_plant = crud.create_plant(db=db, plant=plant)
    return crud.format_plants(created_plant)

@app.get("/filter_plants", response_model = list[schemas.PlantsResponse])
def filter_plants(plant_filter: schemas.PlantFilterRequest = Depends (), db:Session = Depends(get_db)):
    plants = crud.filter_plants(db=db, plant_filter=plant_filter)
    print(plants)
    return [crud.format_plants(plant) for plant in plants]


@app.patch("/update_plant/{plant_id}", response_model=schemas.PlantsResponse)
def update_plant(plant_id: int, info: schemas.PlantUpdate, db:Session = Depends(get_db)):
    plant = crud.update_plant(db=db, plant_id=plant_id, info=info)

    return crud.format_plants(plant)

@app.delete("/delete_plant/{plant_id}", response_model=list[schemas.PlantsResponse])
def delete_plant(plant_id: int, db:Session = Depends(get_db)):
    plants = crud.delete_plant(db = db, plant_id = plant_id)
    # print(plants)
    return [crud.format_plants(plant) for plant in plants]







@app.get("/get_api_data")
def get_api():
    return owm.get_api_data()


# Ang ginagawa lang neto, sinasabe na yung response format ay galing sa schema na Symptoms
# Tapos yung function ay tatangap ng db object galing dun sa get_db function sa taas

