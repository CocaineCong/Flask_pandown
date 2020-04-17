from flask import Blueprint, request
from app.middleware.type_params import FileParams, generate_params, get_params
from app.model.file_model import FileModel
from util import filter_null_dict, time_format, size_pack
from util.response import Successful_response

file_blueprint = Blueprint("file_single_table", __name__, url_prefix="/file")

params: FileParams = generate_params(FileParams)


@file_blueprint.route('/list', methods=["GET"])
def file_list():
    file: FileParams = get_params(request, FileParams, params.parent_path, NN=True)
    c = FileModel.get_file_list(**filter_null_dict(file))
    data = {"items": [
        {params.file_name: i.file_name, params.is_dir: i.is_dir,
         params.update_date: time_format(i.update_date),
         params.size: size_pack(i.size),
         }
        for i in c], params.parent_path: file.parent_path}
    return Successful_response(data=data)


@file_blueprint.route('/rename', methods=["POST"])
def rename():
    file1: FileParams = get_params(request, FileParams, params.file_name, params.parent_path, NN=True)
    file2: FileParams = get_params(request, FileParams, params.new_name)
    FileModel.update_file_name(filter_null_dict(file1), filter_null_dict(file2), params.file_name)
    Successful_response("改名成功")


@file_blueprint.route('/total_size', methods=["GET"])
def total_size():
    file1: FileParams = get_params(request, FileParams, NN=True)
    file2: FileParams = get_params(request, FileParams, params.parent_path)
    temp_dict = filter_null_dict(file1)

    if file2.parent_path == "/":                                           # 计算所有
        total_size = FileModel.get_total_size(temp_dict)
    else:
        temp_dict.update(filter_null_dict(file2))
        total_size = FileModel.get_total_size(temp_dict)

    Successful_response(data=total_size)
