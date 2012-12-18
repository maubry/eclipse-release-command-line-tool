# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import os

_FOLDER_PERMISSIONS = 0775
_FILE_PERMISSIONS = 0664

def contains_products(products_dir_path, product_filenames):
    if os.path.exists(products_dir_path) and os.path.isdir(products_dir_path):
        files_list = os.listdir(products_dir_path)
        for f in files_list:
            if not (os.path.basename(f) in product_filenames):
                return False
        if len(files_list) !=  len (product_filenames):
            return False
        return True
    return False

def set_file_permissions(repository_path):
    os.chmod(repository_path, _FOLDER_PERMISSIONS)
    for root, dirs, files in os.walk(repository_path):
        for d in dirs:  
            os.chmod(os.path.join(root,d), _FOLDER_PERMISSIONS)
        for f in files:
            os.chmod(os.path.join(root,f), _FILE_PERMISSIONS)
