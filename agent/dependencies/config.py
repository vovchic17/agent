from typing import Annotated

from config_reader import Settings
from fastapi import Depends, Request


def get_config(request: Request) -> Settings:
    return request.app.state.config


ConfigDep = Annotated[Settings, Depends(get_config)]
