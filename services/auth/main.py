from fastapi import FastAPI,Depends,HTTPException,status,Security
import jwt, datetime, os,uvicorn
from db import getUser
from pydantic import BaseModel
from typing import Union

from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("DB_HOST"))

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Login(BaseModel):
    email: str
    password: str



app = FastAPI()

@app.get("/alive")
def read_root():
    return {"ack": "1"}

@app.post("/login")
def login(req:Login):

    # check db for username and password
    user=getUser(req.email)

    if user is None or user["password"] != req.password:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials"
        )
    else:
            return createJWT(req.email, os.environ.get("JWT_SECRET_KEY"), True)

from fastapi.security.api_key import APIKeyHeader
token_key = APIKeyHeader(name="Authorization")

class Token(BaseModel):
    token: str

def get_current_token(auth_key: str = Security(token_key)):
    return auth_key

@app.post("/validate")
def validate(current_token: Token = Depends(get_current_token)):

    if not current_token:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials"
        )

    encoded_jwt = current_token.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt,os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"]
        )
    except:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="not authorized"
        )

    return decoded

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == '__main__':
    uvicorn.run("main:app", host=os.environ.get("HOST_URL"), port=8000)