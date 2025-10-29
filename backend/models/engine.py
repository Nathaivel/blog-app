from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends
from .blog import Blog, Comments
from .user import User

db_name = "main.db"
db_url = f"sqlite:///{db_name}"

connect_args = {"check_same_thread":False}
engine = create_engine(db_url,connect_args=connect_args)

def initialize_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDeps = Annotated[Session,Depends(get_session)]