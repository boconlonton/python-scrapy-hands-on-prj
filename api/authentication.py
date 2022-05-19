from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

_API_KEYS = [
    '2f927842-de67-43ae-93cc-41716e01964b'
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in _API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
