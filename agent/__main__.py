import uvicorn
from config_reader import config
from fastapi import Depends, FastAPI
from middlewares import auth_middleware
from routers import router

app = FastAPI(
    title="Агент для поиска лог-файлов",
    dependencies=[Depends(auth_middleware)],
)
app.state.config = config
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=config.PORT)
