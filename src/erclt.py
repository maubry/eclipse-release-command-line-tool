#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import argparse
import sys
from action.milestoneaction import MilestoneAction
from action.stableaction import StableAction

# TODO:
# * Create an option to wipe destination directories when they exist
# * So far, we use a lot of sys.exit(1), maybe it would be nice to have an
#   error code per error type.

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
        description = 'Helps release an Eclipse based product.')

# common parameters
###########################
parser.add_argument('-d', '--directory',
        default = '/',
        help    = 'For tests only, root directory of release process, directory must have a tree similar to build.eclipse.org. Defaults to `/`.',
        metavar = 'root')


# sub parsers (1 by action)
############################
subparsers = parser.add_subparsers(title='All possible release action', help="The possible action, [action] -h to have help")

# milestone action
def deliver_milestone(args):
    print "milestone"

milestone_parser = subparsers.add_parser("m",help= "Deliver a milestone version")
milestone_parser.add_argument('-mv', '--milestoneversion',
        help     = 'New version number, for this milestone release.',
        metavar  = 'version_number',
        required = True)
milestone_parser.set_defaults(func=MilestoneAction())

# stable action
def deliver_stable(args):
    print "stable"

stable_parser = subparsers.add_parser("s", help="Deliver a stable version")
stable_parser.add_argument('-mv', '--milestoneversion',
        help     = 'The milestone version which should be used as new stable release.',
        metavar  = 'version_number',
        required = True)
stable_parser.add_argument('-sv', '--stableversion',
        help     = 'New version number, for this stable release.',
        metavar  = 'version_number',
        required = True)
stable_parser.set_defaults(func=StableAction())

# Parse them all
if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
    print 'All good.'
