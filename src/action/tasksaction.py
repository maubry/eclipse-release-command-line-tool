'''
'''
from locale import str
import sys

class TasksAction():
    
    def gettasks(self,args):
        return []
    
    def __call__(self, args):
        # get all tasks
        tasks = self.gettasks(args)
        
        # check before executing plan
        print "Plan for {0} :".format(self.name())
        for i in range(0,len(tasks)):
            task = tasks[i]
            try:
                print "    Step {0} : {1}.".format(str(i+1),task.name())
                for reportline in task.check():
                    print "        " + reportline                
            except Exception as e:
                print "        ==> Action is not started because {0}: {1} {2}".format(e,type(e),e.args)
                sys.exit()
        
        # execute plan
        print "Execute {0} :".format(self.name())
        for i in range(0,len(tasks)):
            task = tasks[i]
            try:
                print "    Step {0} : {1}.".format(str(i+1),task.name())
                for reportline in task.run():
                    print "        " + reportline      
            except Exception as e:
                print "        ==> Action abort because {0}: {1} {2}".format(e, type(e),e.args)
                sys.exit()

        # done
        print "{0} executed with success.".format(self.name())