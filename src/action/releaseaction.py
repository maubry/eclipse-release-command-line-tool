#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
from action.tasksaction import TasksAction
from tasks.moverepository import MoveRepository
from tasks.moveallrepositorychildren import MoveAllRepositoryChildren

class ReleaseAction(TasksAction):
    def gettasks(self):
        _archive_repo = "c:/Users/sbernard/Documents/tmp/repoEclipse/home/data/httpd/archive.eclipse.org/koneki/releases/stable/ldt/"
        _release_repo = "c:/Users/sbernard/Documents/tmp/repoEclipse/home/data/httpd/download.eclipse.org/koneki/releases/stable/ldt/"
        _milestone_repo = "c:/Users/sbernard/Documents/tmp/repoEclipse/home/data/httpd/download.eclipse.org/koneki/releases/milestones/ldt/"
        
        
                
        return[
               MoveAllRepositoryChildren("Archive Stable Release Repositories",_release_repo, _archive_repo),
               MoveRepository("Deliver new Stable Release Repository",_milestone_repo+"0.9M1", _release_repo+"0.9")
               ] 
        
    def name(self):
        return "Release Action"
