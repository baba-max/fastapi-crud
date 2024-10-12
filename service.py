print("Hello Amazing World")

from models import User
from schema import Usercreateshcema,Userdeletescheme,GetUserschema,UpdateUserschema
from sqlalchemy.orm import Session
from exceptions import UserNotFoundException
import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user_in_db(data:Usercreateshcema,db:Session):
    new_user=User(username=data.username,password=data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"new user is created"}

def delete_user_in_db(data:Userdeletescheme,db:Session):
    user_in_db= db.query(User).filter(User.username==data.username).first()
    if not user_in_db:
        raise UserNotFoundException
    db.delete(user_in_db)
    db.commit()
    return {"msg":"user is deleted"}

def get_user_from_db(*,username:str,db:Session):
    user_from_db=db.query(User).filter(User.username==username).first()
    if not user_from_db:
        raise UserNotFoundException
    else:
        message={"username":user_from_db.username,"password":user_from_db.password}
        return message

def update_user_from_db(user_name:str,new_username:str,data: UpdateUserschema,db:Session):
    user_db=db.query(User).filter_by(username=user_name , password=data.password).first()
    if not user_db:
        raise UserNotFoundException
    user_db.username=new_username
    db.commit()
    db.refresh(user_db)
    return {"message":"username is updated succesfully"}

def delete_all_users(db: Session):
    users = db.query(User).all() 
    if not users:
        raise UserNotFoundException

    for user in users:
        db.delete(user)
    db.commit()

    return {"msg": f"Deleted {len(users)} users"}

def hash_all_users_passwords_service(db: Session):
    users = db.query(User).all()
    if not users:
        return {"msg": "No users found"}

    for user in users:
        if not user.password.startswith("$2b$"):
            user.password = hash_password(user.password)
    db.commit()

    return {"msg": f"Updated passwords for all users which passwords are not hashing"}

def verify_user_credentials(username: str, plain_password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFoundException

    if verify_password(plain_password, user.password):
        return {"msg": "Login successful"}, True
    else:
        return {"msg": "Invalid password"}, False

