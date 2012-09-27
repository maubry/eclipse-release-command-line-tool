#!/usr/bin/python
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import argparse
import os
import os.path
import shutil
import sys
#
# Improvments:
# * Create an option to wipe destination directories when they exist
# * So far, we use a lot of sys.exit(1), maybe it would be nice to have an
#   error code per error type.
#
class Const(object):
    ARCHIVE_MILESTONE =     "products/milestones/"
    ARTIFACT_FILE =         "artifacts.jar"
    CONTENT_FILE =          "content.jar"
    CURRENT_MILESTONE =     "products/current-milestone/"
    MILESTONES_OUTPUT_DIR = "releases/milestones/"
    NIGHTLY_OUTPUT_DIR =    "nightly/"
    LAST_CI_BUILD_PATH =    "/shared/jobs/koneki-ldt/lastSuccessful/archive/product/target/products/"
#
# Defining Actions
#
class MilestoneAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        """Milestone production action"""
        # Compute requested pathes
        if not args.directory.endswith('/'):
            args.directory = "%s/"%args.directory
        nightly_dir = "%s%s"%(args.directory, Const.NIGHTLY_OUTPUT_DIR)
        milestone_dir = "%s%s%s"%(args.directory,
                Const.MILESTONES_OUTPUT_DIR, args.milestone)
        milestone_artifact_path = '%s/%s'%(milestone_dir, Const.ARTIFACT_FILE)
        milestone_content_path  = '%s/%s'%(milestone_dir, Const.CONTENT_FILE)
        archived_milestone_path = '%s%s/%s'%(args.directory,
                Const.ARCHIVE_MILESTONE, args.previousversion)
        current_milestone_path = '%s%s'%(args.directory,
                Const.CURRENT_MILESTONE)
        current_artifact_path = '%s/%s'%(current_milestone_path,
                Const.ARTIFACT_FILE)
        current_content_path = '%s/%s'%(current_milestone_path,
                Const.CONTENT_FILE)
        nightly_files = [nightly_dir,
                '%s/%s'%(nightly_dir, Const.ARTIFACT_FILE),
                '%s/%s'%(nightly_dir, Const.CONTENT_FILE)]

        # Check if destination directory exists
        if os.path.exists(milestone_dir):
            sys.stderr.write('Destination %s already exists.'%milestone_dir)
            sys.exit(1)

        # Check if input directory exists
        for file in nightly_files:
            if not os.path.exists(file):
                print 'Error %s does not exists.'%file
                sys.exit(1)

        # Copy files
        try:
            print 'Copy %s to %s.'%(nightly_dir, milestone_dir)
            shutil.copytree(nightly_dir, milestone_dir)
            print 'Done'
        except Error as ex:
            sys.stderr.stderr.write('Failure: %s.'%ex.message)
            sys.exit(1)

        # Ensure permissions
        files = [milestone_artifact_path, milestone_content_path]
        if not MilestoneAction.check_permissions(milestone_dir, files):
            sys.exit(1)

        # Archive current milestone
        print 'Archiving current milestone.'
        print 'Moving %s to %s.'%(current_milestone_path,
                archived_milestone_path)
        try:
            shutil.copytree(current_milestone_path,
                    archived_milestone_path)
            print 'Done'
        except Error as e:
            print 'Error, unable to archive %s.\n%s'%(
                    current_milestone_path, e.message)
            sys.exit(1)

        # Delivering new version
        print 'Delivering new version'
        try:
            print 'Flushing %s'
            shutil.rmtree(current_milestone_path)
            print 'Done'
            print 'Moving %s to %s.'%(Const.LAST_CI_BUILD_PATH,
                    current_milestone_path)
            shutil.copytree(Const.LAST_CI_BUILD_PATH,
                    current_milestone_path)
            print 'Done'
        except Error as e:
            print 'Error, unable to publish to %s.\n%s'%(
                    current_milestone_path, e.message)
            sys.exit(1)

        # Check files permissions
        files = [current_artifact_path, current_content_path]
        if not MilestoneAction.check_permissions(current_milestone_path, files):
            sys.exit(1)

    @staticmethod
    def check_permissions(parent_folder, files):
        # Checking parent directory
        print 'Setting permissions on %s.'%parent_folder
        try:
            os.chmod(parent_folder, 02765)
            print 'Done'
        except OSError as ex:
            print 'Error, unable to set permissions on %s.\n%s'%(
                    parent_folder, ex.message)
            return False

        # Checking children
        for file in files:
            try:
                print 'Setting permission on %s.'%file
                os.chmod(file, 0664)
            except OSError as e:
                print 'Error, unable to set permissions on %s.\n%s'%(
                        file, e.message)
                return False
        return True

class ReleaseAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        # Release production code
        pass
#
# Define a custom parser to print help when no option has been given
#
class ParserWithHelp(argparse.ArgumentParser):
    def error(self, msg):
        sys.stderr.write('Error: %s\n'%msg)
        self.print_help()
        sys.exit(2)
#
# Dealing with command line arguments
#
parser = ParserWithHelp(
        description = "Helps release an Eclipse based product.",
        epilog      = "So far only milestones are implemented.")
parser.add_argument("-cv", "--currentversion",
        metavar  = ('version_number'),
        required = True,
        help     = "Version being released.")
parser.add_argument("-pv", "--previousversion",
        metavar  = ('previous_version_number'),
        required = True,
        help     = "Previous version released, used for archiving previous version.")
parser.add_argument('-d', '--directory',
        help    = 'All directorie used will be relative to this one, defaults to `./`.',
        default = './',
        metavar = ('dir'))

# Define argument for the type of release we are dealing with.
# There can be only one type handled at once.
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-m", "--milestone",
        action  = MilestoneAction,
        help    = "Indicates that a milestone sould be delivred.",
        nargs   = 0)
group.add_argument("-r", "--release",
        action  = ReleaseAction,
        help    = "Indicates that a release sould be delivred.",
        nargs   = 0)
# Parse them all
args = parser.parse_args()
