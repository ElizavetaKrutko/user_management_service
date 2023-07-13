import uvicorn
from fastapi import Depends, FastAPI

from app.dependencies.database import get_db
from app.rest.routes import app_routes, auth_routes, user_routes

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(app_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
