from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic

security = HTTPBasic()

SecDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]
