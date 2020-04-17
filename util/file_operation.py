import hashlib
import time
import random
import string
import os
from util.response import Error_response


def genRandomString(slen=4):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


def generate_disc_name() -> str:
    return f'{time.time()}-{genRandomString(4)}'


def get_file_md5_size(my_file, block_size=2 * 1024):
    """

    :param my_file: open的file ,rb
    :param block_size: 默认分块大小 2k
    :return: md5,size 以k为单位
    """

    hash = hashlib.md5()
    file_size = 0

    while True:
        data = my_file.read(block_size)
        file_size += len(data)

        if not data:
            break
        hash.update(data)
    hash = hash.hexdigest()

    return hash, file_size / 1024


def save_file(file, save_file_name):
    # 指针归零
    file.seek(0, 0)
    save_file_name = os.path.join(f"{os.getcwd()}\\file_store", save_file_name)
    file.save(save_file_name)


def delete_file(file_name):
    file_real_name = file_exist_in_disc(file_name)
    try:
        os.remove(file_real_name)
    except Exception as e:
        Error_response("删除文件错误", debug_msg=e)


CHUNK_SIZE = 8192


def read_file_chunks(path):
    with open(path, 'rb') as fd:
        while 1:
            buf = fd.read(CHUNK_SIZE)
            if buf:
                yield buf
            else:
                break


def file_exist_in_disc(file_name):
    file_name = os.path.join(f"{os.getcwd()}\\file_store", file_name)
    if os.path.exists(file_name):
        return file_name
    else:
        Error_response("该文件不存在", debug_msg=file_name)
