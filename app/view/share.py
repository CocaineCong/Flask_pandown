import uuid
import time
import random
from app import redis
from app.model.share_model import ShareModel
from app.model.ShareAnalysis import ShareAnalysis
from flask import Blueprint, session, request
from app.middleware.type_params import ShareParams, Share_Anal_Params, generate_params, get_params
from util.file_operation import genRandomString
from util import filter_null_dict

share = Blueprint("share", __name__, url_prefix="/file")
params_Ana: Share_Anal_Params = generate_params(Share_Anal_Params)


@share.route('/share_uuid', methods=['POST', 'GET'])
def file_uuid():
    file_u = f"{uuid.uuid1()}{genRandomString(4)}"  # 生成uuid
    print(file_u)
    vaild_date: Share_Anal_Params = get_params(request, Share_Anal_Params,params_Ana.file_path,params_Ana.file_name,NN=True)
    #pool = redis.ConnectionPool(host='127.0.0.1', port=5000, db=0)  # 设置过期时间
    #r = redis.StrictRedis(connection_pool=pool)
    #redis.expire(vaild_date.file_name, 60)
    vaild_date.file_uuid=file_u
    ShareModel(**filter_null_dict(vaild_date)).add()
    return file_u


@share.route('/share_good')
def share_good():
    count_good: Share_Anal_Params = get_params(request, Share_Anal_Params, params_Ana.file_share_count)
    count_good+=1
    return count_good

# download
#2. uuid =》 file_real_address -->fil——name  #如何获取文件下载
#1. pre_download uuid passwd => filename  size  #渲染页面

