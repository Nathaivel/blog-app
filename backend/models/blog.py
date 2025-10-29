from sqlmodel import SQLModel,Field, ForeignKey,Relationship
from typing import List,Optional

#devlog 2
class Comments(SQLModel,table=True):
    id: int = Field(primary_key=True)
    content: str
    user_id: int = Field(ForeignKey("User.id"))
    blog_id: int = Field(foreign_key="blog.id")
    blog: Optional["Blog"] = Relationship(back_populates="comments")
    
#devlogs 1
class Blog(SQLModel,table=True):
    id: int = Field(primary_key=True,index=True)
    title: str = Field(index=True)
    body: str = Field()
    user: int = Field(ForeignKey("User.id"))
    comments: List["Comments"] = Relationship(back_populates="blog")
