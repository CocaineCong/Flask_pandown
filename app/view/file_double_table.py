from flask import Blueprint, request, stream_with_context, Response
from app.middleware.type_params import FileParams, generate_params, get_params
from app.model.disc_model import DiscModel
from app.model.file_model import FileModel
from util import filter_null_dict
from util.response import Successful_response
from util.file_operation import *

file_blueprint = Blueprint("file_double_table", __name__, url_prefix="/file")

params: FileParams = generate_params(FileParams)  # 传值的源头


@file_blueprint.route('/create_folder', methods=["POST"])
@file_blueprint.route('/upload', methods=["POST"])
def upload():
    file: FileParams = get_params(request, FileParams, params.file_name, params.is_dir, params.parent_path, NN=True)
    file.size, file.disc_id = None, None
    # TODO 考虑提取
    if (not file.file_name == None) and (not file.file_name.find("/") == -1):
        Error_response("错误的文件名,文件夹名")

    if (not file.parent_path == None) and (not file.parent_path.startswith("/")):
        Error_response("错误的路径")

    if not file.is_dir:
        # 不是目录
        files = request.files  #
        my_file = files.get(params.file)
        if my_file == None:
            Error_response.you_ip_has_been_recorded()
        file.file_name = my_file.filename
        file.md5, file.size = get_file_md5_size(my_file)
        d = DiscModel.find_md5(file.md5)
        if d[0]:
            # 如果数据库中没有这条
            disc_name = generate_disc_name()
            save_file(my_file, disc_name)
            # 增加 返回 id
            # 不值得使用type_params修改,因为要创建一个新的对象,然后去赋值,不如直接赋值
            file.disc_id = DiscModel(md5=file.md5, disc_name=disc_name).id
        else:
            # 如果数据库中有这条
            file.disc_id = d[1]
            DiscModel.count_crease(file.disc_id, is_add=True)
        my_file.close()
    print(file.md5)
    FileModel(**filter_null_dict(file, exclude={params.md5})).add()
    return Successful_response("创建/上传成功")


@file_blueprint.route('/download', methods=["POST"])
def download():
    file: FileParams = get_params(request, FileParams, params.file_name, params.parent_path, NN=True)
    disc_id = FileModel.get_disc_id(**filter_null_dict(file))
    disc_name = DiscModel.get_disc_name(disc_id)
    disc_full_name = file_exist_in_disc(disc_name)
    return Response(
        stream_with_context(read_file_chunks(disc_full_name)),
        headers={
            'Content-Disposition': f'attachment; filename={file.file_name}'
        }
    )


@file_blueprint.route('/delete', methods=["POST"])
def file_delete():
    file: FileParams = get_params(request, FileParams, params.file_name, params.parent_path, NN=True)
    disc_is_dir, disc_id = FileModel.delete_file_record(filter_null_dict(file))
    if not disc_is_dir:
        count, disc_name = DiscModel.count_crease(disc_id, is_add=False)
        if count <= 0:
            DiscModel.delete_sql(DiscModel, dict(id=disc_id))
            delete_file(disc_name)
    return Successful_response("删除成功")
