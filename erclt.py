#!/usr/bin/python2.6
import argparse
import os.path
import shutil
import sys
#
# Improvements:
# * Create an option to wipe destination directories when they exist
# * So far, we use a lot of sys.exit(1), maybe it would be nice to have an
#   error code per error type.
#
class Const(object):
	MILESTONES_OUTPUT_DIR = "/releases/milestones/"
	NIGHTLY_OUTPUT_DIR =    "/nightly/"
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
		milestone_dir = "%s%s%s"%(
			args.directory,
			Const.MILESTONES_OUTPUT_DIR,
			args.milestone)

                # Check if destination directory exists
		if os.path.exists(milestone_dir):
			sys.stderr.write('Destination %s already exists.'%milestone_dir)
			sys.exit(1)

		# Check if input directory exists
		if not os.path.exists(nightly_dir):
                        sys.stderr.write('Input %s does not exists.'%nightly_dir)
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
			
class ReleaseAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
                # Release production code
                pass
#
# Define a custom parser to print help when no option has been given
#
class ParserWithHelp(argparse.ArgumentParser):
	def error(self, msg):
		sys.stderr.write('error: %s\n' % msg)
		self.print_help()
		sys.exit(2)
#
# Dealing with command line arguments
#
parser = ParserWithHelp(
	description = "Helps release an Eclipse based product.")
parser.add_argument("-m", "--milestone",
	action=MilestoneAction,
	help="Indicates that a milestone sould be delivred",
	metavar=('milestone'))
parser.add_argument("-n", "--number",
	metavar=('versionnumber'),
	required=True,
	help="Version of release")
parser.add_argument('-d', '--directory',
	help='Directory where operations will take place, defaults to `.`.',
	action='store_const',
	const = '.',
	metavar=('dir'))
args = parser.parse_args()
