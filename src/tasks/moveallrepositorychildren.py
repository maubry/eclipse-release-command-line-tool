'''
 task use to move all children of a composite repository to another
'''
import repositoryutils
class MoveAllRepositoryChildren:
    
    def __init__(self, name, source, dest):
        self._name = name
        self._source = source
        self._dest = dest
    
    def check(self):
        report  = []
        # check if source is a composite repository
        if not repositoryutils.is_composite_repository(self._source):
            raise Exception("source {0} is not a composite repository".format(self._source))
        
        # check if destination is a composite repository 
        if not repositoryutils.is_composite_repository(self._dest):
            raise Exception("destination {0} is not a composite repository".format(self._dest))
        
        # check there are no conflicts
        for child_name in repositoryutils.composite_repository_list_child(self._source):
            if repositoryutils.composite_repository_contains(self._dest, child_name):
                raise Exception("destination {0} already contains a child {1}".format(self._dest,child_name))
            else:
                report.append("Repo {0} will be moved from {1} to {2}:".format(child_name,self._source,self._dest))
        
        if len(report) == 0:
            report.append("No child to move ...")
            
        return report
        
    def run(self):
        report  = []
        # move all children
        for child_name in repositoryutils.composite_repository_list_child(self._source):
            repositoryutils.move_child_from_composite_repository(self._source, self._dest, child_name,child_name)
            report.append("{0} moved".format(child_name))

        if len(report) == 0:
            report.append("Nothing to do.")
            
        return report       
            
    def name(self):
        return self._name