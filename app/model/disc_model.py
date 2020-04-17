from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from util.response import Error_response
from app import db
from ._base_model import BaseModel, BaseDao, none_none


class DiscModel(BaseModel, BaseDao):
    """
    磁盘 表
    """
    __tablename__ = 'disc'
    md5 = Column(String(64))
    disc_name = Column(String(64))
    count = Column(Integer)

    def __init__(self, md5=None, count=1, disc_name=None):
        self.md5 = md5
        self.count = count
        self.disc_name = disc_name
        if none_none(md5, disc_name):
            super(DiscModel, self).add()

    @classmethod
    def find_md5(cls, md5):
        """
        :return: 如果找的到 返回 false 否则 返回 true
        """
        c = super(DiscModel, cls).normal_find_one(cls, dict(md5=md5))
        if c == None:
            return (True, None)
        else:
            return (False, c.id)

    @classmethod
    def get_disc_name(cls, id):
        c = super(DiscModel, cls).force_find_one(cls, dict(id=id))
        return c.disc_name

    @classmethod
    def count_crease(cls, id, is_add=True):
        """
        increase  增 decrease 少
        这个函数是一个特殊的函数,因为写入频繁,为避免并发带入的麻烦,引入锁
        :param id:
        :return:
        """
        condition = dict(id=id)
        # 悲观锁 多写少读
        c = super(DiscModel, cls).lock_find_one(cls, condition)
        if is_add:
            c.count += 1
        else:
            c.count -= 1
        db.session.commit()
        return (c.count, c.disc_name)
