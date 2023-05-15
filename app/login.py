# from fastapi import APIRouter, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext



# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


# def get_hash_password(plain_password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hash_password):
#     return pwd_context.verify(plain_password, hash_password)



# router = APIRouter()


# @router.post("/login/token", tags=["login"])
# def get_token_after_authentication(form_data: OAuth2PasswordRequestForm = Depends()):
# 	print(form_data.username)
# 	print(form_data.password)