import hashlib
from app.model.person_model import PersonModel
from pydantic import BaseModel
class TestClass(BaseModel,PersonModel):
    pass
print(TestClass)


def get_file_md5_size(my_file, block_size= 2* 1024):
    hash = hashlib.md5()
    file_size = 0
    with my_file as file:

        while True:
            data = file.read(block_size)
            file_size+=len(data)

            if not data:
                break
            hash.update(data)
    hash = hash.hexdigest()
    return hash,file_size/1024
f= open("flask_file_share.rar","rb")


c = get_file_md5_size(f)
print(c)