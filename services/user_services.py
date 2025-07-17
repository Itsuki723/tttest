from sqlalchemy import Select

from models.usermodel import UserModel
from common.extensions import db

                                        #后续考虑更新：密码加密存储、注册功能实现
class UserService:
    def login(self,username:str,password:str):
        query = Select(UserModel).where(UserModel.username==username)
        user_model = db.session.scalars(query).first()
        if user_model and user_model.password == password:
            return user_model
        else:
            return None

    def register_user(self, username:str,password:str):
        query = Select(UserModel).where(UserModel.username==username)
        exist_user = db.session.scalars(query).first()

        if exist_user:
            raise Exception(f"user {username} already exist")

        new_user = UserModel(username=username,password=password)

        db.session.add(new_user)
        db.session.commit()

        return new_user