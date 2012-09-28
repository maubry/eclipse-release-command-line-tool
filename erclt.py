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
            args.directory = '{0}/'.format(args.directory)
        nightly_dir = '{0}{1}'.format(args.directory, Const.NIGHTLY_OUTPUT_DIR)
        milestone_dir = "{0}{1}{2}".format(args.directory,
                Const.MILESTONES_OUTPUT_DIR, args.newversion)
        milestone_artifact_path = '{0}/{1}'.format(milestone_dir, Const.ARTIFACT_FILE)
        milestone_content_path  = '{0}/{1}'.format(milestone_dir,
                Const.CONTENT_FILE)
        archived_milestone_path = '{0}{1}{2}'.format(args.directory,
                Const.ARCHIVE_MILESTONE, args.oldversion)
        current_milestone_path = '{0}{1}'.format(args.directory,
                Const.CURRENT_MILESTONE)
        current_artifact_path = '{0}{1}'.format(current_milestone_path,
                Const.ARTIFACT_FILE)
        current_content_path  = '{0}{1}'.format(current_milestone_path,
                Const.CONTENT_FILE)
        nightly_files = [nightly_dir,
                '{0}/{1}'.format(nightly_dir, Const.ARTIFACT_FILE),
                '{0}/{1}'.format(nightly_dir, Const.CONTENT_FILE)]

        # Check if destination directory exists
        if os.path.exists(milestone_dir):
            sys.stdout.write('Destination {0} already exists.'.format(
                milestone_dir))
            sys.exit(1)

        # Check if input directory exists
        for file in nightly_files:
            if not os.path.exists(file):
                sys.stdout.write('Error {0} does not exists.'.format(file))
                sys.exit(1)

        # Check artifacts path
        if not os.path.exists(args.artifactspath):
            sys.stdout.write('There are no artifacts at {0}.\n'.format(
                args.artifactspath))
            sys.exit(1)

        # Copy files
        try:
            sys.stdout.write('Copy {0} to {1}: '.format(nightly_dir, milestone_dir))
            shutil.copytree(nightly_dir, milestone_dir)
            sys.stdout.write('Done\n')
        except OSError as ex:
            sys.stdout.write('Failure\n%s'%ex.message)
            sys.exit(1)

        # Ensure permissions
        files = [milestone_artifact_path, milestone_content_path]
        if not MilestoneAction.check_permissions(milestone_dir, files):
            sys.exit(1)

        # Archive current milestone
        sys.stdout.write('Archiving current milestone.\n')
        try:
            sys.stdout.write('Creating directory {0}: '.format(archived_milestone_path))
            sys.stdout.write('Done\n')
            sys.stdout.write('Moving {0} to {1}: '.format(current_milestone_path,
                archived_milestone_path))
            shutil.copytree(current_milestone_path, archived_milestone_path)
            sys.stdout.write('Done\n')
        except OSError as e:
            sys.stdout.write('Error\nUnable to archive %s.\n%s'%(
                current_milestone_path, e.strerror))
            sys.exit(1)

        # Delivering new version
        sys.stdout.write('Delivering new version.\n')
        try:
            sys.stdout.write('Flushing {0}: '.format(current_milestone_path))
            shutil.rmtree(current_milestone_path)
            sys.stdout.write('Done\n')

            sys.stdout.write('Copying {0} to {1}: '.format(args.artifactspath
                ,current_milestone_path))
            shutil.copytree(args.artifactspath, current_milestone_path)
            sys.stdout.write('Done\n')
        except OSError as e:
            sys.stdout.write('Error\nUnable to publish to {0}.\n1{}'.format(
                current_milestone_path, e.strerror))
            sys.exit(1)

        # Check files permissions
        files = [current_artifact_path, current_content_path]
        if not MilestoneAction.check_permissions(current_milestone_path, files):
            sys.exit(1)

    @staticmethod
    def check_permissions(parent_folder, files):
        # Checking parent directory
        sys.stdout.write('Setting permissions on {0}: '.format(parent_folder))
        try:
            os.chmod(parent_folder, 02765)
            sys.stdout.write('Done\n')
        except OSError as ex:
            sys.stdout.write('Error.\nUnable to set permissions on {0}.\n{1}'\
                    .format(parent_folder, ex.message))
            return False

        # Checking children
        for file in files:
            try:
                sys.stdout.write('Setting permissions on {0}: '.format(file))
                os.chmod(file, 0664)
                sys.stdout.write('Done\n')
            except OSError as e:
                sys.stdout.write('Error\nUnable to set permissions on {0}.\n{1}'\
                        .format(file, e.strerror))
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
        sys.stdout.write('Error: {0}\n'.format(msg))
        self.print_help()
        sys.exit(2)
#
# Dealing with command line arguments
#
parser = ParserWithHelp(
        description = 'Helps release an Eclipse based product.',
        epilog      = 'So far only milestones are implemented.')
parser.add_argument('-ov', '--oldversion',
        help     = 'New version number, the one being released.',
        metavar  = 'version_number',
        required = True)
parser.add_argument('-nv', '--newversion',
        help     = 'Previously released version number, used for archiving it.',
        metavar  = 'version_number',
        required = True)
parser.add_argument('-d', '--directory',
        default = './',
        help    = 'All directories used will be relative to this one, defaults to `./`.',
        metavar = 'dir')
parser.add_argument('-ap', '--artifactspath',
        default = Const.LAST_CI_BUILD_PATH,
        help    = 'Path to the artifacts to release, often last sucessful build form continuous integration.',
        metavar = 'path_to_artifacts',
        nargs   = '?')

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
