from fastapi import FastAPI
from app.routes.v1 import user

# from app.routes import auth
# from app.routes import user
application = FastAPI()
application.include_router(user.router) 
app = application

