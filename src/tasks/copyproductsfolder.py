'''
    copy products folder from a folder to another
'''
import shutil
from tasks.moveproductsfolder import MoveProductsFolder
import productutils
class CopyProductsFolder(MoveProductsFolder):
    
    def check(self):
        MoveProductsFolder.check(self)
        return ["Products will be copied from {0} to {1}".format(self._source_path,self._dest_path)]       
    
    def run(self):
        shutil.copytree(self._source_path, self._dest_path)
        
        productutils.set_file_permissions(self._dest_path)
        
        return ["Products copied."]                       