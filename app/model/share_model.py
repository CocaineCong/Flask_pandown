from sqlalchemy import Column, String, Integer, DateTime
from ._base_model import BaseModel, BaseDao
from app.middleware.type_params import ShareParams
import datetime


class ShareModel(BaseModel, BaseDao):
    __tablename__ = 'share'
    user_name = Column(String(64))
    file_name = Column(String(64))
    file_uuid = Column(String(64))
    update_time = Column(DateTime, default=datetime.datetime.now())
    vaild_time = Column(DateTime, default=datetime.datetime.now()+datetime.timedelta(days=1)) #过期时间
    file_path = Column(String(64))
