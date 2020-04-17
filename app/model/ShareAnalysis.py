from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean
from ._base_model import BaseModel, BaseDao, none_none
from app.middleware.type_params import Share_Anal_Params
import datetime


class ShareAnalysis(BaseModel,BaseDao):
    __tablename__ = 'ShareAnalysis'
    share_id = Column(Integer)
    file_good = Column(Integer)
    file_path = Column(String(64))
    file_share_count = Column(Integer)
    #share link
    # 1   13 1
    # 1   1 2
    # 1   1 3
