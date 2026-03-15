from fastapi import FastAPI
from starlette.middleware import Middleware
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.todos_routes import router as todos_routes
from middleware.middleware import JWTMiddleware

app = FastAPI(middleware=[
        Middleware(JWTMiddleware)])

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todos_routes)