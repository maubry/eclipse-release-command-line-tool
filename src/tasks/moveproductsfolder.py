'''
    move products folder from a folder to another
'''
import os
import shutil
import productutils

class MoveProductsFolder:
    def __init__(self, name, source_path, dest_path,product_filenames):
        self._name = name
        self._source_path = source_path
        self._dest_path = dest_path
        self._product_filenames = product_filenames
    
    def check(self):
        # check source folder
        self._parent_source_path = os.path.dirname(self._source_path)
        if not os.path.isdir(self._parent_source_path):
            raise Exception("source {0} is not a directory".format(self._parent_source_path))
        
        # check destination folder
        self._parent_dest_path = os.path.dirname(self._dest_path)
        if not os.path.isdir(self._parent_dest_path):
            raise Exception("destination {0} is not a directory".format(self._parent_dest_path))

        # check folder to move is a folder 
        if not os.path.isdir(self._source_path):
            raise Exception("folder {0} which must be moved is not a directory".format(self._source_path))
        
        # check  folder contains products
        if not productutils.contains_products(self._source_path, self._product_filenames): 
            raise Exception("folder {0} which must be moved does not contains the given products {1}".format(self._source_path,self._product_filenames))
        
        # check destination is empty
        if os.path.exists(self._dest_path):
            raise Exception("a file or folder {0} already exists".format(self._dest_path))
         
        return ["Products folder will be moved from {0} to {1}".format(self._source_path,self._dest_path)]    
        
        
    def run(self):
        shutil.move(self._source_path, self._dest_path)
        
        productutils.set_file_permissions(self._dest_path)
        
        return ["Products folder moved.".format(self._source_path,self._dest_path)]   
                
    def name(self):
        return self._name