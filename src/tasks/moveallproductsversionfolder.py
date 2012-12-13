'''
    move all products folder from a folder to another
'''
import os
import shutil
import productutils
class MoveAllProductVersionFolder:
    def __init__(self, name, source_path, dest_path,product_filenames):
        self._name = name
        self._source_path = source_path
        self._dest_path = dest_path
        self._product_filenames = product_filenames
    
    def check(self):
        report= []
        
        # check source folder
        if not os.path.isdir(self._source_path):
            raise Exception("source {0} is not a directory".format(self._source_path))
        
        # check destination folder
        if not os.path.isdir(self._dest_path):
            raise Exception("destination {0} is not a directory".format(self._dest_path))

        # check folder to move is a folder
        for file_name in os.listdir(self._source_path):
            full_path = os.path.join(self._source_path,file_name)
            if os.path.isfile(full_path):
                raise Exception("products folder {0} contains files, and should only contains directory".format(self._source_path)) 
            if not productutils.contains_products(full_path, self._product_filenames):
                raise Exception("folder {0} which must be moved does not contains the given products {1}".format(full_path,self._product_filenames))
        
        # check folder child folder
        for sf in os.listdir(self._source_path):
            if sf in  os.listdir(self._dest_path):
                raise Exception("destination folder {0} already contains a folder {1}".format(sf,self._dest_path,sf))
            else:
                report.append("Products {0} will be moved from {1} to {2}".format(sf,self._source_path,self._dest_path))
           
        if len(report) == 0:
            report.append("No child to move ...")     
                
        return report  
        
        
    def run(self):
        report =[]
        
        for sf in os.listdir(self._source_path):
            shutil.move(os.path.join(self._source_path,sf),os.path.join(self._dest_path,sf))
            report.append("Products {0} moved.".format(sf))
        
        #TODO change file permissions
        if len(report) == 0:
            report.append("No products to move ...")
        
        return report
                
    def name(self):
        return self._name