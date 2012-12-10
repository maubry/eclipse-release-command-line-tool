#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
from milestoneaction import MilestoneAction
import argparse
import sys
from action.releaseaction import ReleaseAction

# TODO:
# * Create an option to wipe destination directories when they exist
# * So far, we use a lot of sys.exit(1), maybe it would be nice to have an
#   error code per error type.
# * At the beginning of MilestoneAction, there a lot of pathes defined, we
#   should take time to comment how the look like.

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
        default = '/',
        help    = 'Root directory of release process, directory must have an arborescence similar to build.eclipse.org. Defaults to `/`.',
        metavar = 'root')

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
if __name__ == '__main__':
    args = parser.parse_args()
    print 'All good.'
