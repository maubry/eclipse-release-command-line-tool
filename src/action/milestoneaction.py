#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
from action.tasksaction import TasksAction
from eclipsefs import EclipseFS
from tasks.publishrepository import PublishRepository
from tasks.copyproductsfolder import CopyProductsFolder

class MilestoneAction(TasksAction):
    def gettasks(self,args):
        
        efs = EclipseFS(args.directory)
        milestone_version = args.milestoneversion
	project_name = "koneki"
        product_name = "ldt"
	remote_name = "remote"
        
        return[PublishRepository("Publish new Milestones Release Repositories",
                                        efs.nightly_repository(product_name),
                                        efs.release_milestones_composite_repository(product_name),
                                        milestone_version,
                                        efs.stats_uri(project_name),
                                        [efs.feature_id(product_name),efs.feature_id(remote_name)]
                                        ),
               CopyProductsFolder("Deliver new Milestones Products",
                                        efs.nightly_products_directory(product_name),
                                        efs.release_milestones_products_directory(product_name, milestone_version),
                                        efs.products_filenames(product_name))] 
        
    def name(self):
        return "Milestone Action"
