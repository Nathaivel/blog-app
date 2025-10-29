from models import engine
from sqlmodel import select, text
from fastapi import APIRouter,Query,HTTPException,Depends
from typing import Annotated
from routers import user

router = APIRouter(prefix="/blogs")

@router.get("/")
def get_all_blog_posts(session: engine.SessionDeps,offset :int = 0,limit :Annotated[int, Query(le=100)] = 100):
    blogs = session.exec(select(engine.Blog).offset(offset).limit(limit)).all()
    return blogs


@router.post("/new")
def add_new_blog_post(session: engine.SessionDeps,blog: engine.Blog,user: Annotated[engine.User,Depends(user.get_current_user)]):
    blog.user = user.id
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return {"msg":"success 200"}
 
 
@router.get("/{id}")
def get_blog_post_by_id(id: int,session: engine.SessionDeps):
     blog = session.get(engine.Blog,id)
     
     if not blog:
         raise HTTPException(404,"Blog post not found")
     
     return blog

@router.delete("/{id}")
def delete_blog_post(id: int,session: engine.SessionDeps):
    temp = get_blog_post_by_id(id,session)
    session.delete(engine.Blog,id)
    
    return {"msg":f"Succesfully deleted blog with id {id}"}
    
@router.put("/{id}")
def update_blog_post(id: int,blog: engine.Blog,session: engine.SessionDeps,user: Annotated[engine.User,Depends(user.get_current_user)]):    
    
    old_blog = get_blog_post_by_id(id,session)
    
    if(old_blog.user != user.id):
        raise HTTPException(401,"Unauthorized access")
        
    
    old_blog.title = blog.title
    old_blog.body = blog.body
    
    session.add(old_blog)
    session.commit()
    session.refresh(old_blog)
    
    return {"msg":f"Succesfully updated blog with id {id}"}
 
 
 #Comments
 
@router.post("/{id}/comments/add")
def add_comment_to_blog(id: int,session: engine.SessionDeps,user: Annotated[engine.User,Depends(user.get_current_user)],comment: engine.Comments):
     comment.user_id = user.id
     comment.blog_id = id
     
     session.add(comment)
     session.commit()
     session.refresh(comment)
     
     return {"msg":f"New comment added at blog {id} by {user.name}"}
     
     
@router.get("/{id}/comments/")
def get_comments_in_blog(id: int,session: engine.SessionDeps):
    comments = session.exec(select(engine.Comments).where(text(f"blog_id={id}"))).all()
    
    if not comments:
        raise HTTPException(404,"Blog post not found")
    
    return comments