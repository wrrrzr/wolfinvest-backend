from typing import Optional

from fastapi import Depends, HTTPException, Request

from app.utils.jwt import verify_jwt_token


def get_token_from_cookies(request: Request) -> Optional[str]:
    return request.cookies.get("token")


def get_user_id(token: Optional[str] = Depends(get_token_from_cookies)) -> int:
    if token is None:
        raise HTTPException(status_code=401, detail="You don't have token")

    data = verify_jwt_token(token)

    if data is None:
        raise HTTPException(status_code=401, detail="Unknown token")

    return data["id"]
