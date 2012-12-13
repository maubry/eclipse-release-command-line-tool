# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import os

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

