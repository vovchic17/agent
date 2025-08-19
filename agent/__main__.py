import uvicorn
from fastapi import FastAPI

from config_reader import config
from routers import router

app = FastAPI(title="Агент для поиска лог-файлов")
app.state.config = config
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, port=config.PORT)
