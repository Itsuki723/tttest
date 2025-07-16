from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from common.extensions import db


class UserModel(db.Model):          #后续更新：考虑密码加密存储
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    username:Mapped[String] = mapped_column(String(128),nullable=False,unique=True)
    password:Mapped[String] = mapped_column(String(128),nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }
