#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import argparse
from   consts import Const
from   eclipsefs import EclipseFS
import os
import releaseutils
import shutil
from   StringIO import StringIO
import sys
import zipfile

# TODO:
# * Create an option to wipe destination directories when they exist
# * So far, we use a lot of sys.exit(1), maybe it would be nice to have an
#   error code per error type.
# * At the beginning of MilestoneAction, there a lot of pathes defined, we
#   should take time to comment how the look like.

#
# Defining Actions
#
class MilestoneAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        """Milestone production action"""

        # Compute requested pathes
        eclipsefs = EclipseFS(args.oldversion, args.newversion, args.directory)

        # Check if destination directory exists
        new_milestone = eclipsefs.new_milestone()
        if os.path.exists(new_milestone):
            print 'Destination {0} already exists.'.format( new_milestone )
            sys.exit(1)

        # Check if input directory exists
        for file in eclipsefs.nightly_jars():
            if not os.path.exists(file):
                print 'Error {0} does not exists.'.format( file )
                sys.exit(1)

        # Check product directory path
        ci_product = eclipsefs.ci_product()
        if not os.path.exists(ci_product):
            print 'There is no continuous integration product folder {0}.'\
                    .format(ci_product)
            sys.exit(1)

        # Check products path
        productslist = [ os.path.join(ci_product, product)
                for product in os.listdir(eclipsefs.ci_product())
                    if os.path.isfile(os.path.join(eclipsefs.ci_product(), product))]
        for product in eclipsefs.ci_products():
            if not os.path.exists(product):
                print 'Product {0} does not exist.'.format( product )
                sys.exit(1)

        # Copy files
        try:
            nightly = eclipsefs.nightly()
            new_milestone_nightly = eclipsefs.new_milestone()
            sys.stdout.write( 'Copy {0} to {1}: '.format(nightly, new_milestone_nightly) )
            shutil.copytree(nightly, new_milestone_nightly)
            sys.stdout.write('Done\n')
            milestone_parent = os.path.dirname(os.path.normpath(new_milestone_nightly))
            sys.stdout.write('Setting permissions on repository parent {0}: '\
                    .format(milestone_parent))
            os.chmod(milestone_parent, Const.FOLDER_PERMISSIONS)
            sys.stdout.write('Done\n')
        except OSError as ex:
            sys.stdout.write('Error.\n{0}'.format(ex))
            sys.exit(1)

        # XML fun
        try:
            #
            # Activate statistics on repository
            #
            # TODO: The lines below might be written elsewhere

            #Read from archive
            milestone_artifact_path = eclipsefs.new_milestone_artifacts()
            sys.stdout.write('Opening {0}: '.format(milestone_artifact_path))
            updatedxmlbuffer = StringIO()
            artifactzip = zipfile.ZipFile(milestone_artifact_path)
            sys.stdout.write('Done\nReading {0}: '.format(
                milestone_artifact_path))
            artifactfilecontent = artifactzip.read(Const.ARTIFACT_MANIFEST)
            artifactzip.close()

            # Updating xml            
            sys.stdout.write('Done\nActivating statistics in {0}: '.format(
                Const.ARTIFACT_MANIFEST))
            releaseutils.activatestats(artifactfilecontent, updatedxmlbuffer)

            # Writing in archive
            sys.stdout.write('Done\nSaving statistics to {0} in {1}: '.\
                    format(Const.ARTIFACT_MANIFEST, milestone_artifact_path))
            artifactzip = zipfile.ZipFile(milestone_artifact_path, 'w')
            artifactzip.writestr(Const.ARTIFACT_MANIFEST,
                    updatedxmlbuffer.getvalue())
            sys.stdout.write('Done\n')

            #
            # Updating repository compositeArtifacts.xml and
            # compositeContent.xml to tell p2 about this version
            #
            for xml_file_path in eclipsefs.milestones_xml_files():

                # Compute path
                sys.stdout.write('Updating {0}: '.format(xml_file_path))

                # Read content
                xmlfile = open(xml_file_path)
                xml = xmlfile.read()
                xmlfile.close()

                # Update xml
                xml = releaseutils.addxmlchild(xml, args.newversion)

                # Save xml
                xmlfile = open(xml_file_path, 'w')
                xmlfile.write(xml)
                xmlfile.close()
                sys.stdout.write('Done\n')

            #
            # Update parent directory XML to notify that there is a repository
            # nested in 'ldt' folder
            #
            filelist = {
                eclipsefs.milestone_composite_content():
                    releaseutils.compositecontentxml(args.newversion),
                eclipsefs.milestone_composite_artifacts():
                    releaseutils.compositeartifactsxml(args.newversion)
            }
            for xmlfilepath, xmlcontent in filelist.items():

                # Creating up-to-date XML
                xmlcontent = releaseutils.addxmlchild(xmlcontent,
                        os.path.normpath(EclipseFS.LDT_SUB_DIRECTORY))

                # Create files
                sys.stdout.write('Creating {0}: '.format(xmlfilepath))
                file = open(xmlfilepath, 'w')
                file.write(xmlcontent)
                file.close()
                sys.stdout.write('Done\n')

        except ValueError as e:
            sys.stdout.write('Error.\nUnable to handle XML.\n{0}'.format(e))
            sys.exit(1)
        except IOError as e:
            sys.stdout.write('Error.\nUnable to read.\n{0}'.format(e))
            sys.exit(1)
        finally:
            artifactzip.close()
            updatedxmlbuffer.close()

        # Ensure permissions
        files = eclipsefs.new_milestone_xml_files()
        if not releaseutils.checkpermissions(eclipsefs.new_milestone(), files):
            for f in files:
                print 'Unable to set permissions on {0}.'.format( f )
            sys.exit(1)

        # Archive current milestone
        print 'Archiving current milestone.'
        product_current_milestone = eclipsefs.product_current_milestone()
        product_archive = eclipsefs.product_archive()
        try:
            sys.stdout.write('Moving {0} to {1}: '.format(
                product_current_milestone, product_archive))
            shutil.copytree(product_current_milestone, product_archive)
            sys.stdout.write('Done\n')
        except OSError as e:
            sys.stdout.write('Error\nUnable to archive {0}.\n{1}\n'.format(
                product_current_milestone, e))
            sys.exit(1)

        # Delivering new version
        print 'Delivering new version.'
        try:
            sys.stdout.write('Flushing {0}: '.format(
                product_current_milestone))
            shutil.rmtree(product_current_milestone)
            sys.stdout.write('Done\n')

            sys.stdout.write('Copying products to {0}: '.format(
                product_current_milestone))
            os.mkdir(product_current_milestone)
            for product in productslist:
                shutil.copy(product, product_current_milestone)
            sys.stdout.write('Done\n')
        except OSError as e:
            sys.stdout.write('Error\nUnable to publish to {0}.\n{1}\n'.format(
                product_current_milestone, e))
            sys.exit(1)

        # Check files permissions
        if not releaseutils.checkpermissions(product_current_milestone,
                productslist):
            print 'Error.\nUnable to set permissions on {0}.'.format(
                    product_current_milestone)
            sys.exit(1)

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
