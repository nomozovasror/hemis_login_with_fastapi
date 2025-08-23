from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
import httpx
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import schemas, crud, models
from .database import get_db
from .dependencies import create_access_token

load_dotenv()

UNIVER = os.getenv("UNIVER")
OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
OAUTH2_REDIRECT_URI =os.getenv("OAUTH2_REDIRECT_URI")


router = APIRouter(prefix="/users", tags=["users"])
@router.get("/login")
async def hemis_login_teacher():
    auth_url = (
        f"https://hemis.{UNIVER}.uz/oauth/authorize?response_type=code"
        f"&client_id={OAUTH2_CLIENT_ID}"
        f"&redirect_uri={OAUTH2_REDIRECT_URI}"
    )
    return RedirectResponse(url=auth_url)

@router.get("/auth")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://hemis.{UNIVER}.uz/oauth/access-token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "code": code,
                "client_id": OAUTH2_CLIENT_ID,
                "client_secret": OAUTH2_CLIENT_SECRET,
                "redirect_uri": OAUTH2_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch access token: {response.text}"
            )
        tokens = response.json()
        access_token = tokens.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Access token not found in response")

        user_info_url = f"https://hemis.{UNIVER}.uz/oauth/api/user"
        response = await client.get(
            user_info_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to fetch user info: {response.text}"
            )

        user_info = response.json()

        employee_id = user_info.get("employee_id_number")
        user_data = schemas.UserBase(
            employee_id=employee_id,
            name=user_info.get("name", ""),
            login=user_info.get("login", ""),
            picture=user_info.get("picture", ""),
            first_name=user_info.get("first_name", ""),
            surname=user_info.get("surname", ""),
            patronymic=user_info.get("patronymic", ""),
            birthday=user_info.get("birthday", ""),
            phone=user_info.get("phone", "")
        )

        db_user = crud.get_user_by_employee_id(db, employee_id)
        if not db_user:
            db_user = crud.create_user(db, user_data)

        roles = user_info.get("roles", [])
        role_codes = [role["code"] for role in roles]

        for role in roles:
            db_role = crud.get_role_by_code(db, role["code"])
            if not db_role:
                role_data = schemas.RoleBase(code=role["code"], name=role["name"])
                db_role = crud.create_role(db, role_data)
            if db_role not in db_user.roles:
                crud.assign_role_to_user(db, db_user, db_role)

        access_token = create_access_token(data={"sub": employee_id, "roles": role_codes})
        return {"access_token": access_token, "token_type": "bearer"}



