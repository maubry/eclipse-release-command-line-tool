#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import argparse
from   consts    import Const
from   eclipsefs import EclipseFS
import os
import releaseutils
import shutil
import sys
import tempfile
import urllib2
import zipfile

class CheckConsts:
    ARTIFACT_FILE           = 'archive.zip'
    ARTIFACT_FOLDER         = 'repository/'
    LAST_ECLIPSE_REPOSITORY = 'https://hudson.eclipse.org/hudson/job/koneki-ldt/lastSuccessfulBuild/artifact/product/target/repository/*zip*/repository.zip'
    LAST_ECLIPSE_PRODUCT    = 'https://hudson.eclipse.org/hudson/view/All/job/koneki-ldt/lastSuccessfulBuild/artifact/product/target/products/'

def download(url, dst):
    """Download provided url to a file at provided file path."""
    try:
        artifact_file = open(dst, 'w+b')
        remote_file = urllib2.urlopen(url)
        shutil.copyfileobj(remote_file, artifact_file)
    except IOError as e:
        print e
        shutil.rmtree(dst)
        return False
    finally:
        artifact_file.close()
        remote_file.close()
    return True

# Creating parsing arguments
parser = argparse.ArgumentParser(
        description='Create an arborensce similar to build.eclipse.org in order to test deploy script safely.')
parser.add_argument('-a', '--artifacts',
        help    = 'Zip file which contains the `repository/` folder available under `konekisources/product/target/`.',
        metavar = 'repository_zip',
        nargs   = '?')
parser.add_argument('-p', '--products',
        help    = 'Product archives to place in arborescence.',
        metavar = 'procuct_archive',
        nargs   = '*')
arguments = parser.parse_args()

# TODO Is it useful to create an EclipseFS implementation for testing?
eclipsefs = EclipseFS(0, 0)
print 'Everything will happen under temporary folder {0}.'.format(
        eclipsefs.root())

# Ensure we have a products list
internetproducts = False
if not arguments.products:
    internetproducts =  True
    arguments.products = ['{0}{1}'.format(CheckConsts.LAST_ECLIPSE_PRODUCT, x)
            for x in EclipseFS.PRODUCT_ARCHIVE_FILENAMES]
else:
    # Ensure user provided products files exist
    for prod in arguments.products:
        if not os.path.exists(prod):
            print 'Product {0} does not exist.'.format(prod)
            shutil.rmtree(eclipsefs.root())
            sys.exit(1)

# Ensure we got an artifact
filepath = ''
if arguments.artifacts:
    if os.path.exists(arguments.artifacts):
        filepath = arguments.artifacts
        print 'Using artifacts available at {0}.'.format(filepath)
    else:
        print '{0} does not exists.'.format(arguments.artifacts)
        shutil.rmtree(eclipsefs.root())
        sys.exit(1)
else:
    # Downloading last sucessful build
    filepath = os.path.join(eclipsefs.ci_repository(), CheckConsts.ARTIFACT_FILE)
    print 'Downloading {0} under {1}.'.format(
            CheckConsts.LAST_ECLIPSE_REPOSITORY, filepath)
    try:
        # Creating directory
        os.makedirs(eclipsefs.ci_repository(), Const.FOLDER_PERMISSIONS)
        download(CheckConsts.LAST_ECLIPSE_REPOSITORY, filepath)
    except IOError as e:
        print e
        shutil.rmtree(eclipsefs.root())
        sys.exit(1)
    print 'Successfully downloaded to {0}.'.format(filepath)

# Downloading products
tempproducts = []
if internetproducts:
    # Creating directory for product download
    try:
        product_folder = eclipsefs.ci_product()
        print 'Creating {0}.'.format( product_folder )
        os.makedirs( product_folder )
    except OSError as e:
        print 'Unable to create {0}.\n{1}'.format(product_folder, e)
        shutil.rmtree(eclipsefs.root())
        sys.exit(1)

    tempproducts = eclipsefs.ci_products()
    for i in range(len(tempproducts)):
        print 'Downloading {0}\n\tto {1}.'.format(arguments.products[i],
                tempproducts[i])
        if not download(arguments.products[i], tempproducts[i]):
            print 'Unable to downloading {0} to {1}.'.format(arguments.products[i],
                    tempproducts[i])
            shutil.rmtree(eclipsefs.root())
            sys.exit(1)

    # Use downloaded products
    arguments.products = tempproducts
    print 'All products are downloaded.'

# Unzipping artifacts
artifact_zip = zipfile.ZipFile(filepath)
try:
    ci = eclipsefs.ci()
    print 'Unzipping {0} under {1}.'.format(filepath, ci)
    artifact_zip.extractall(ci)
    print 'Unzipped under {0}.'.format(ci)
except IOError as e:
    print 'Unable to extract {0} under {1}.\n{2}'.format(filepath, ci, e)
    shutil.rmtree(eclipsefs.root())
    sys.exit(1)
finally:
    artifact_zip.close()

# Creating file tree
try:
    # Creating directories
    milestones = eclipsefs.milestones()
    os.makedirs(milestones)
    print '{0} created.'.format(milestones)

    #
    # Creating p2 xml
    #

    files = {
        eclipsefs.milestones_composite_content():
            releaseutils.compositecontentxml(),
        eclipsefs.milestones_composite_artifacts():
            releaseutils.compositeartifactsxml()
    }
    for xml_file_path, content in files.iteritems():

        # Creating parent folder
        directory = os.path.dirname(xml_file_path)
        if not os.path.exists( directory ):
            print 'Creating {0}.'.format( directory )
            os.makedirs( directory )

        # Creating XML files
        print 'Creating {0}.'.format(xml_file_path)
        xmlfile = open(xml_file_path, 'w')
        xmlfile.write(content)
        xmlfile.close()

    # Copying artifacts under right directories
    nightly = eclipsefs.nightly()
    print 'Copying artifacts files from {0} to {1}.'.format(
            eclipsefs.ci_repository(), nightly)
    shutil.copytree(eclipsefs.ci_repository(), nightly)
    print 'Copy of update-site available under {0}.'.\
            format(nightly)

    # Packing products
    product_milestone = eclipsefs.product_current_milestone()
    os.makedirs(product_milestone)
    print 'Packing products in {0}.'.format(product_milestone)
    for product in arguments.products:
        shutil.copy(product, product_milestone)
    print 'Products available under {0}.'.format(product_milestone)

    # Copy products to continuous integration
    ci_product = eclipsefs.ci_product()
    print 'Creating {0}.'.format( ci_product )
    os.makedirs(ci_product)
    print 'Packing products in continuous integration under {0}.'.format(
            ci_product)
    for product in arguments.products:
        if internetproducts:
            shutil.move(product, ci_product)
        else:
            shutil.copy(product, ci_product)
    print 'Products available under {0}.'.format(ci_product)
except OSError as e:
    print 'Unable create test tree, {0}. '.format(e)
    root = eclipsefs.root()
    print 'Flushing {0}.'.format( root )
    shutil.rmtree( root )
    sys.exit(1)
print 'All good, available under {0}.'.format( eclipsefs.root() )
