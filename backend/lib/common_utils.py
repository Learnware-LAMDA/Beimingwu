import zipfile
import os
import shutil
import hashlib


def get_top_folder_in_zip(zfile: zipfile.ZipFile):
    """
    Get the top folder in a zip file.
    """
    top_folders = set()
    for name in zfile.namelist():
        if name.endswith("/"):
            # it is a folder
            name = name[:-1]
            if "/" not in name:
                # it is a top folder
                top_folders.add(name)
                pass
            pass
        else:
            if "/" not in name:
                # it is a top file
                return ""
            pass
        pass

    if len(top_folders) == 1:
        return top_folders.pop() + "/"
    else:
        return ""
    pass


def delete_folder_content(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            pass
        pass
    pass


def get_file_hash(filename: str) -> str:
    """
    Get the md5 value of a file.
    """

    md5 = hashlib.md5()
    with open(filename, "rb") as fin:
        while True:
            data = fin.read(1024 * 1024)
            if len(data) == 0:
                break
            md5.update(data)
            pass
        pass
    return md5.hexdigest()
