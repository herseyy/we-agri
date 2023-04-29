"""
Main file
"""
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# from fastapi.templating import Jinja2Templates

from . import crud, models, schemas, owm
from .database import SessionLocal, engine

from pydantic import BaseModel

# Matic nagccreate na ng table
models.Base.metadata.create_all(bind=engine)
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



##### USERS

@app.post("/create_user", response_model = schemas.UserResponse)
def create_user(user: schemas.UserRequest, db:Session = Depends(get_db)):
    created_user = crud.create_user(db=db, user=user)
    # print(crud.format_user(created_user))
    return crud.format_user(created_user)

@app.get("/filter_users", response_model = list[schemas.UserResponse])
def filter_users(user_filter: schemas.UserFilterRequest = Depends(), db:Session = Depends(get_db)):
    users = crud.filter_users(db, user_filter)
    # for user in users:
    #     print(crud.format_user(user))
    return [crud.format_user(user) for user in users]





##### PLANTS

@app.post("/create_plant", response_model = schemas.PlantsResponse)
def create_plant(plant: schemas.PlantRequest, db:Session = Depends(get_db)):
    created_plant = crud.create_plant(db=db, plant=plant)
    return created_plant


@app.get("/get_api_data")
def get_api():
    return owm.get_api_data()



# Ang ginagawa lang neto, sinasabe na yung response format ay galing sa schema na Symptoms
# Tapos yung function ay tatangap ng db object galing dun sa get_db function sa taas


