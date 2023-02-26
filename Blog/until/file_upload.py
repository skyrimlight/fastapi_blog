from fastapi import UploadFile, File
from time import time
from Blog.until.setting import BASE_DIR


def upload_file_one(file):
    file_new_name = str(int(time())) + file.filename.replace(" ", '')
    file_data = file.file.read()
    with open(BASE_DIR + '/' + file_new_name, 'wb') as f:
        f.write(file_data)
    return {"filename": file_new_name, "content_type": file.content_type}
