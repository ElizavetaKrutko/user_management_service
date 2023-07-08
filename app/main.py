from fastapi import Depends, FastAPI

from app.db.dependencies.database import get_async_session
from app.rest import app_routes, auth_routes, user_routes

# import uvicorn


app = FastAPI(dependencies=[Depends(get_async_session)])

app.include_router(app_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)


# if __name__ == "__main__":
#    uvicorn.run(app, host="localhost", port=8000)
