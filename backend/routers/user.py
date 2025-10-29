from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select, text
from models import engine
from typing import Annotated
import json 
import random
import hashlib
from datetime import datetime, timedelta

def searchdictlist(lis,key,value):
    try:
        search_result = [l[key] == value for l in lis]
        print("Searh results: ",search_result)
        index = search_result.index(True)
        
        return index
    except KeyError:
        return None
    except ValueError:
        print("No search results")
        return None





router = APIRouter(prefix="/users")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

try:
    with open("tokens.json","r") as file:
        tokens = json.load(file)
        now = datetime.utcnow()
        
        for token in tokens:
            if datetime.fromisoformat(token["expiry"]) < now:
                tokens.remove(token)
                
except FileNotFoundError:
    tokens = []

def generate_token():
    token = random.randbytes(64).hex()
    return token

def new_token(user: engine.User):
    with open("tokens.json","w") as file:
        expiry = datetime.utcnow() + timedelta(seconds=3600)
        token = generate_token()
        temp_token = {"user_id":user.id,"token":token,"expiry":datetime.isoformat(expiry)}
        tokens.append(temp_token)
        json.dump(tokens,file,indent=4)
        return temp_token
 
def validate_token(token):
    token_index = searchdictlist(tokens,"token",token)
    now = datetime.utcnow()
    
    
    if token_index == None:
        return None
    
    token_expiry = datetime.fromisoformat(tokens[token_index]["expiry"])
    print("IS NOT EXPIRED: ",token_expiry > now)
   
    if token_expiry > now:
        return tokens[token_index]["user_id"]
    else:
        return None
            
            
    
async def get_current_user(session: engine.SessionDeps,token: Annotated[str, Depends(oauth_scheme)]):
    
    user = session.get(engine.User,validate_token(token))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
    

@router.post("/token")
async def get_token(session: engine.SessionDeps,form_data: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = session.exec(select(engine.User).where(text(f"name='{form_data.username}'"))).all()
    
    if not user:
        raise HTTPException(401,"Username or password invalid")
    
    user = user[0]
    
    if user.hashed_password != hashlib.sha256(form_data.password.encode() + form_data.username.encode()).hexdigest():
        raise HTTPException(401,"Username or password invalid")
        
        
    return {"token": new_token(user)}
    

@router.get("/me")
async def get_me(user: Annotated[engine.User,Depends(get_current_user)]):
    return user

@router.post("/add")
async def add_user(session: engine.SessionDeps,user: engine.User):
    """if me.id != 1:
        raise HTTPException("Not admin/User do not have proper credentials",401)"""
    
    user.hashed_password = hashlib.sha256(user.hashed_password.encode() + user.name.encode()).hexdigest()
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"msg": f"Successfully added user {user.name} at id {user.id}"}