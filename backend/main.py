from fastapi import FastAPI
from models import engine
from routers import blog, user

#hjfv
app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)

@app.on_event("startup")
def start_server():
    engine.initialize_db()
    
   
@app.get("/")
def main_endpoint(session: engine.SessionDeps):
    return {"hey":"you reached the main endpoint"}
