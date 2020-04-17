from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from app import db
from sqlalchemy.exc import IntegrityError
import re
from util.response import Error_response


def none_none(first, end):
    return first != None and end != None


# model  类的本体
class BaseModel(db.Model):
    __abstract__ = True  # 抽象类
    id = Column(Integer, primary_key=True, autoincrement=True)


# dao sql 就是增删查改
class BaseDao(object):

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            # 特殊情况处理

            c = re.match("\(sqlite3.IntegrityError\) UNIQUE constraint failed: (\w*\.\w*)", str(e))

            if c != None:
                Error_response.duplicate_data(c.group(1))
            raise e
        except Exception as e:
            raise e

    def find_all(self, original_data, error_response=None):
        c = self.query.filter_by(**original_data).all()

        if len(c) == 0 and error_response == None:
            return False
        if len(c) == 0:
            return error_response(debug_msg=original_data)
        return c

    def normal_find_one(self, original_data):
        return self.query.filter_by(**original_data).first()

    def force_find_one(self, original_data, return_object=None):
        c = self.query.filter_by(**original_data)
        f = c.first()
        if f == None:
            raise Error_response.not_find_in_sql(original_data)
        if not return_object:
            return f

        else:
            return c

    def lock_find_one(self, original_data):
        """
        带锁去查找 方便后期更新 互斥锁
        :param original_data:
        :return:
        """
        c = self.query.filter_by(**original_data).with_for_update(read=True).first()
        if c == None:
            Error_response.not_find_in_sql(debug_msg=original_data)
        else:
            return c

    def update(self, original_data, will_update_data):

        try:
            c = self.force_find_one(self, original_data, return_object=True)
            c.update(will_update_data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_sql(self, original_data):
        try:
            c = self.force_find_one(self, original_data, return_object=True)
            c.delete()
            db.session.commit()
        except Exception as e:
            raise e
