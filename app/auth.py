from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# from .server import get_db
from .models import User
from .crud import verify_password, get_hash_password
from jose import JWTError, jwt 

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="pages")


SECRET_KEY = "83e8c4bb007a0fa49d3157792dfaaf94125ff85b5057bbcf306a4980a7383d9b"   #ilagay sa env
ALGORITHM = "HS256"  # ito rin


def get_db(request: Request):
    return request.state.db

@router.get("/loginsss")
def login(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})


@router.post("/loginsss")
async def login(response: Response, request: Request, db:Session=Depends(get_db)):
	form = await request.form()
	username = form.get("username")
	password = form.get("password")
	errors = []
	if not username:
		errors.append("Please enter valid username")
	if not password or len(password):
		errors.append("Password should be > 5 character")
	try:
		user = db.query(User).filter(User.username == username).first()
		if user is None:
			errors.append("No username")
			return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
		else:
			if verify_password(password, user.hashed_pass):
			    data = {
			        "sub": username
			    }
			    jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
			    msg = "Login Successful"
			    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
			    response.set_cookie(key = "access_token", value = f"Bearer {jwt_token}", httponly=True)
			    return response 
			else:
				errors.append("Invalid Password")
				return templates.TemplateResponse("login.html", {"request": request, "errors": errors})
	except:
		errors.append("Something Wrong")
		return templates.TemplateResponse("login.html", {"request": request, "errors": errors})


# @app.get('/cookie')
# async def cookie(response: Response):

# 	# It work
# 	response.set_cookie(key="test", value="example")
# 	return {"result": "ok"}
# @router.get("/")
# 
# @router.post("/")