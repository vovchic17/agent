from dependencies import ConfigDep, SecDep
from fastapi import HTTPException


def auth_middleware(
    config: ConfigDep,
    creds: SecDep,
) -> None:
    if (
        creds.username != config.AUTH_USERNAME
        or creds.password != config.AUTH_PASSWORD
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")
