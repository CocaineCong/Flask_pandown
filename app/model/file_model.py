from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy import func
from util.response import Error_response
from ._base_model import BaseModel, BaseDao, none_none
import datetime
from typing import Dict, Tuple
from app import db


class FileModel(BaseModel, BaseDao):
    __tablename__ = 'file'
    user_name = Column(String(64))
    file_name = Column(String(64))
    update_date = Column(DateTime, default=datetime.datetime.now())
    disc_id = Column(Integer)
    is_dir = Column(Boolean)
    parent_path = Column(String(64))
    size = Column(String(64))

    @classmethod
    def duplicate_file_name(cls, user_name, file_name, parent_path):
        condition = {"user_name": user_name, "file_name": file_name, "parent_path": parent_path}
        c = super(FileModel, cls).normal_find_one(cls, condition)
        if c != None:
            Error_response.duplicate_file_name(debug_msg=condition)

    @classmethod
    def get_file_list(cls, **kwargs):
        return super(FileModel, cls).find_all(cls, kwargs, error_response=Error_response.get_file_list_none)

    @classmethod
    def get_disc_id(cls, **kwargs):
        c = super(FileModel, cls).force_find_one(cls, kwargs)
        return c.disc_id

    @classmethod
    def delete_file_record(cls, condition: Dict) -> Tuple[bool, int]:
        c = super(FileModel, cls).force_find_one(cls, condition, return_object=True)
        q = c.first()
        i, d = q.is_dir, q.disc_id
        c.delete()
        db.session.commit()
        return (i, d)

    @classmethod
    def get_total_size(cls, condition: Dict):
        c = db.session.query(func.sum(cls.size)).filter_by(**condition)
        return c.scalar()

    @classmethod
    def update_file_name(cls, condition: Dict, will_update_data: Dict, file_name_string: str):
        will_update_data = {file_name_string: list(will_update_data.values())[0]}
        c = super(FileModel, cls).update(cls, condition, will_update_data)
