from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_employee_id(db: Session, employee_id: int):
    return db.query(models.User).filter(models.User.employee_id == employee_id).first()

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(
        employee_id=user.employee_id,
        name=user.name,
        login=user.login,
        picture=user.picture,
        first_name=user.first_name,
        surname=user.surname,
        patronymic=user.patronymic,
        birthday=user.birthday,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_role_by_code(db: Session, code: str):
    return db.query(models.Role).filter(models.Role.code == code).first()

def create_role(db: Session, role: schemas.RoleBase):
    db_role = models.Role(code=role.code, name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def assign_role_to_user(db: Session, user: models.User, role: models.Role):
    user.roles.append(role)
    db.commit()
    db.refresh(user)
    return user