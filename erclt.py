#!/usr/bin/python2.6
import argparse
#
# Defining Actions
#
class MilestoneAction(argparse.Action):
	def __call__(self, parser, args, values, option_string=None):
		# Milestone production code
		pass
class ReleaseAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
                # Release production code
                pass
#
# Dealing with command line arguments
#
parser = argparse.ArgumentParser(
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
