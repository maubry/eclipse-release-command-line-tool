'''
 task use to move a repository from a composite repository to another
'''
import repositoryutils
import os
class MoveRepository:
    
    def __init__(self, name, source_path, dest_path):
        self._name = name
        self._source_path = source_path
        self._dest_path = dest_path
    
    def check(self):
        # check if source is a composite repository
        self._source_parent_path = os.path.dirname(self._source_path)
        self._source_name = os.path.basename(self._source_path)
        if not repositoryutils.is_composite_repository(self._source_parent_path):
            raise Exception("source {0} is not a composite repository".format(self._source_parent_path))
        
        # check if source composite repository contains the repository to move
        if not repositoryutils.composite_repository_contains(self._source_parent_path, self._source_name):
            raise Exception("source repository {0} does not contain a child {1}".format(self._source_parent_path,self._source_name))
        
        # check if destination is a composite repository 
        self._dest_parent_path = os.path.dirname(self._dest_path)
        self._dest_name = os.path.basename(self._dest_path)
        if not repositoryutils.is_composite_repository(self._dest_parent_path):
            raise Exception("destination {0} is not a composite repository".format(self._dest_parent_path))
        
        # check if destination does not already contains the repository to move
        if repositoryutils.composite_repository_contains(self._dest_parent_path, self._dest_name):
            raise Exception("destination {0} already contains a child {1}".format(self._dest_parent_path,self._dest_name))
        
        return ["Repo {0} will be moved to {1}".format(self._source_path,self._dest_path)]            
        
    def run(self):
        repositoryutils.move_child_from_composite_repository(self._source_parent_path,self._dest_parent_path, self._source_name,self._dest_name)
        return ["Repo {0} moved".format(self._dest_name)]
            
    def name(self):
        return self._name