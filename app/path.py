
import os
from Directory.settings import DIRECTORY_TO_BROWSE


def get_abs_root():
    return get_abs_path(DIRECTORY_TO_BROWSE)


def is_inside_root(eventual_path):
    virtual_root = get_abs_root()
    return os.path.commonprefix([virtual_root, eventual_path]) == virtual_root


def get_abs_path(path):
    return os.path.abspath(os.path.realpath(path))


def get_names(directory):
    """Returns list of file names within directory"""
    contents = os.listdir(directory)
    files, directories = [], []
    for item in contents:
        candidate = os.path.join(directory, item)
        if os.path.isdir(candidate):
            directories.append(item)
        else:
            files.append(item)
    return files, directories


def get_rel_path(path):
    if is_inside_root(get_abs_path(path)):
        link_target = os.path.relpath(path, start=get_abs_root())
    else:
        link_target = None
    return link_target


def get_content(directory):
    """Returns list of file names within directory"""
    contents = os.listdir(directory)
    files, directories = [], []
    for item in contents:
        candidate = os.path.join(directory, item)
        if os.path.isdir(candidate):
            directories.append(item)
        else:
            files.append(item)
    return files, directories


streaming_file_type={
    'mp4':('video','video/mp4'),
    'mov':('video','video/mp4'),
    'webm':('video','video/webm'),
    'mp3':('audio','audio/mpeg'),
    'wav':('audio','audio/wav'),
    'jpeg':('image',''),
    'jpg':('image',''),
    'gif':('image',''),
    'png':('image',''),
    'bmp':('image',''),
    'svg':('image',''),
}

def streaming_file(path):
    if not os.path.isfile(path):
        return ('','')
    else:
        file_name = os.path.basename(path)
        if file_name.rfind('.') == -1:
            return ('','')
        postfix = file_name[file_name.rfind('.')+1:].lower()
        if postfix in streaming_file_type:
            return streaming_file_type[postfix]
        else:
            return ('','')





