"""
Main file
"""
from fastapi import FastAPI, Request, Response, Depends, HTTPException, Query, status, File, UploadFile
from typing import Optional, Annotated, Union
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
# from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import crud, models, schemas, owm, auth
from .database import SessionLocal, engine
import os
from fastapi.responses import FileResponse


# from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm




# from passlib.context import CryptContext

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta


import uuid





# Matic nagccreate na ng table
models.Base.metadata.create_all(bind=engine)


# SECRET_KEY = "4882fb01f85938a7b77a1cc157c84a4b3cee06e069ce6bc880235755f190de18"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Main app object
app = FastAPI()

IMAGEDIR = "./static/images/plants/"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")

app.include_router(auth.router)


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



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


# def get_hash_password(plain_password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hash_password):
#     return pwd_context.verify(plain_password, hash_password)

from jose import jwt

SECRET_KEY = "83e8c4bb007a0fa49d3157792dfaaf94125ff85b5057bbcf306a4980a7383d9b"   #ilagay sa env
ALGORITHM = "HS256"  # ito rin


# jwt_token = ""

import requests

@app.get("/")
def index(token:str=Depends(crud.oauth2_scheme)):
    return {"Hello": "World"}

@app.post("/login", tags=["login"])
def get_token_after_authentication(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Incorrect username", headers={"WWW-Authenticate": "Bearer"})
    if not crud.verify_password(form_data.password, user.hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Incorrect password", headers={"WWW-Authenticate": "Bearer"})
    data = {
        "sub": form_data.username
    }
    jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key = "access_token", value = f"Bearer {jwt_token}", httponly = True)



    return {"access_token": jwt_token, "token_type": "bearer"}


##### USERS

# , response_model = schemas.UserResponse
@app.post("/create_user", response_model = schemas.SignUpResponse)
def create_user(user: schemas.SignUpRequest, db:Session = Depends(get_db)):
    created_user = crud.create_user(db=db, user=user)
    # print(created_user)
    if created_user == None:
        raise HTTPException(404, detail="Username is already taken")
        # return {"message": "username is taken"}

    return created_user
    # return crud.format_user(created_user)

@app.get("/filter_users", response_model = list[schemas.UserResponse])
def filter_users(user_filter: schemas.UserFilterRequest = Depends(), q: Union[list[int], None] = Query(default=None), db:Session = Depends(get_db)):
    users = crud.filter_users(db, user_filter, q)
    # for user in users:    
    #     print(crud.format_user(user))
    return [crud.format_user(user) for user in users]



@app.patch("/update_user")
def update_user(info: schemas.UserUpdateRequest, db: Session = Depends(get_db)):
    # print("jwt_token")
    # print(crud.token_)
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    updated_user = crud.update_user(db=db, current_user=user, info=info)

    return crud.format_user(updated_user)


@app.patch("/change_pass")
def change_pass(pass_:schemas.UserChangePass, db:Session = Depends(get_db), token:str=Depends(crud.oauth2_scheme)):
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    updated_pass_user = crud.change_pass(db=db, current_user=user, pass_=pass_)

    return updated_pass_user


@app.get("/get_all_user_plants", response_model=list[schemas.UserPlantsResponse])
def get_all_user_plants(db: Session = Depends(get_db)):
    user_plants = db.query(models.UserPlants).all()

    # plants = crud.get_user_plants(db=db, user_plants = user_plants)

    # print(user_plants)
    # return [crud.format_plants(plant) for plant in plants]
    return [crud.format_user_plants(plant) for plant in user_plants]

@app.get("/filter_user_plants", response_model=list[schemas.UserPlantsResponse])
def filter_user_plants(user_plant_filter: schemas.UserPlantsFilter = Depends(), db:Session = Depends(get_db), token:str=Depends(crud.oauth2_scheme)):

    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    # user_plants = db.query(models.UserPlants).filter(models.UserPlants.user_id == user.id).all()
    filtered_user_plants = crud.filter_user_plants(user=user, db=db, user_plant_filter=user_plant_filter)
    # print(user_plants)
    # plants = crud.get_user_plants(db=db, user_plants=user_plants)

    # return [crud.format_plants(plant) for plant in plants]
    return [crud.format_user_plants(plant) for plant in filtered_user_plants]



# @app.get("/filter_users", response_model = list[schemas.UserResponse])
# def filter_users(user_filter: schemas.UserFilterRequest = Depends(), q: Union[list[int], None] = Query(default=None), db:Session = Depends(get_db)):
#     users = crud.filter_users(db, user_filter, q)
#     # for user in users:    
#     #     print(crud.format_user(user))
#     return [crud.format_user(user) for user in users]





@app.delete("/delete_user_plant/{plant_id}", response_model=list[schemas.UserPlantsResponse])
def delete_user_plant(plant_id: int, db:Session = Depends(get_db), token:str=Depends(crud.oauth2_scheme)):
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    plants = crud.delete_user_plant(db=db, user_id= user.id, plant_id= plant_id)

    return [crud.format_user_plants(plant) for plant in plants]



# @app.get("/filter_users", response_model = list[schemas.UserResponse])
# def filter_users(user_filter: schemas.UserFilterRequest = Depends(), q: Union[list[int], None] = Query(default=None), db:Session = Depends(get_db)):
#     users = crud.filter_users(db, user_filter, q)
#     # for user in users:    
#     #     print(crud.format_user(user))
#     return [crud.format_user(user) for user in users]

@app.get("/user/{username}", response_model = schemas.UserResponse)
def get_current_user(username:str, db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)
    no_plants = len(user.plants)
    print(no_plants)
    username = user.username
    return crud.format_user(user)


# @app.get("/user/{username}/plants", response_model=list[schemas.CurrentUserPlants])
# def get_current_user_plants(username:str, db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
#     user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

#     my_plants = crud.get_current_user_plants(user=user, db=db)
#     return my_plants

@app.get("/user/{username}/plants/filter", response_model=list[schemas.CurrentUserPlants])
def get_current_user_plants(username:str, plants_filter: schemas.FilterCurrentUserPlants = Depends(), db: Session = Depends(get_db), token: str = Depends(crud.oauth2_scheme)):
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    my_plants = crud.get_current_user_plants_filter(user=user, db=db, filter_plants=plants_filter)
    return my_plants




@app.delete("/delete_user")
def delete_user(pass_: str, db: Session = Depends(get_db), token:str=Depends(crud.oauth2_scheme)):

    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    mess = crud.delete_user(db = db, user_id = user.id, pass_=pass_)

    return mess

@app.post("/add_user_plant/{plant_id}")
def add_user_plant(plant_id: int, plant_info: schemas.UserPlantsRequest, db:Session = Depends(get_db), token:str=Depends(crud.oauth2_scheme)):
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    plants = crud.add_user_plant(db=db, plant_info=plant_info, current_user= user, plant_id= plant_id)

    message = {
        "message": "user already has this plant"
    }

    if plants is False:
        return {"message": "No user found"}

    if plants is None or plants == []:
        return message

    return [crud.format_plants(plant) for plant in plants]  
    

@app.patch("/update_user_plant/{plant_id}", response_model=schemas.UserPlantsResponse)
def update_user_plant(plant_id: int, plant_info: schemas.UserPlantUpdate, db:Session = Depends(get_db), token:str=Depends(crud.oauth2_scheme)):
    user = crud.decode(token, SECRET_KEY, ALGORITHM, db)

    plant = crud.update_user_plant(db=db, plant_info=plant_info, current_user= user, plant_id= plant_id)

    return crud.format_user_plants(plant)


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





@app.post("/upload/{name}")
async def create_upload_file(name:str, file: UploadFile = File(...), db:Session = Depends(get_db)):

    file.filename = f"{name}.jpg"
    contents = await file.read()

    # save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    image_path = f"{IMAGEDIR}{file.filename}"
    # print(image_path)

    plant = db.query(models.Plant).filter(models.Plant.name == name).first()

    plant.file_path = image_path
    db.commit()

    return {"filename": file.filename}


@app.get("/show_img/{name}")
async def read_file(name:str, db:Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.name == name).first()
    path = plant.file_path
    # path = f"{IMAGEDIR}{name}.jpg"
    # print(path)
    return FileResponse(path)




@app.get("/login", response_class=HTMLResponse)
async def submit(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

