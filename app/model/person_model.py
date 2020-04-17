from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from util.response import Error_response
from ._base_model import BaseModel, BaseDao, db, none_none


class PersonModel(BaseModel, BaseDao):
    __tablename__ = 'person'
    name = Column(String(64), unique=True, nullable=False)
    passwd = Column(String(64), nullable=False)

    @classmethod
    def update_passwd(cls, name, passwd, new_passwd):
        new_passwd = generate_password_hash(new_passwd)
        c = PersonModel.find_by_user_passwd(name, passwd)
        c.passwd = new_passwd
        db.session.commit()

    @classmethod
    def find_by_user_passwd(cls, name, passwd):
        c = super(PersonModel, cls).force_find_one(cls, dict(name=name))
        if c == None:
            Error_response.user_not_exits()
        if not check_password_hash(c.passwd, passwd):
            Error_response.password_wrong()
        return c
