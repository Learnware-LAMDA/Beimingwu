import zipfile

def get_top_folder_in_zip(zfile: zipfile.ZipFile):
    """
    Get the top folder in a zip file.
    """
    top_folders = set()
    for name in zfile.namelist():
        if name.endswith('/'):
            # it is a folder
            name = name[:-1]
            if '/' not in name:
                # it is a top folder
                top_folders.add(name)
                pass
            pass
        else:
            if '/' not in name:
                # it is a top file
                return ''
            pass
        pass

    if len(top_folders) == 1:
        return top_folders.pop() + '/'
    else:
        return ''
    pass