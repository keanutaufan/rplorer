from typing import Annotated, Union
from fastapi import Cookie, status, HTTPException

from app.utils.token import decode_access_token

async def get_sub(Authorization: Annotated[Union[str, None], Cookie()] = None):
    if Authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not logged in",
        )
    
    try:
        decoded = decode_access_token(Authorization)
        return decoded["sub"]
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is logged out 1",
        )