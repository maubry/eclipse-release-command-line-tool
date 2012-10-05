#!/usr/bin/python2.6
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import argparse
from   consts import Const
import os
import shutil
import sys
import tempfile
import urllib2
import zipfile
class CheckConsts:
    ARTIFACT_FILE_PATH      = 'archive.zip'
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
        shutil.rmtree(tmpdir)
        return False
    finally:
        artifact_file.close()
        remote_file.close()
    return True

# Creating parsing arguments
parser = argparse.ArgumentParser(
        description='Create the files properly to run deploy script.')
parser.add_argument('-a', '--artifacts',
        help    = 'Artifacts zip file path',
        metavar = 'artifacts_zip_path',
        nargs   = '?')
parser.add_argument('-p', '--products',
        help  = 'List of archived products to deploy.',
        nargs = '*')
arguments = parser.parse_args()
tmpdir = tempfile.mkdtemp()
print 'Everything will happen under temporary folder {0}.'.format(tmpdir)

# Ensure we have a products list
internetproducts = False
if not arguments.products:
    internetproducts =  True
    arguments.products = \
            ['{0}{1}'.format(CheckConsts.LAST_ECLIPSE_PRODUCT, x)
                    for x in Const.PRODUCT_ARCHIVE_FILENAMES]
else:
    # Ensure user provided products files exist
    for prod in arguments.products:
        if not os.path.exists(prod):
            print 'Product {0} does not exist.'.format(prod)
            shutil.rmtree(tmpdir)
            sys.exit(1)

# Ensure we got an artifact
filepath = ''
if arguments.artifacts:
    if os.path.exists(arguments.artifacts):
        filepath = arguments.artifacts
        print 'Using artifacts available at {0}.'.format(filepath)
    else:
        print '{0} does not exists.'.format(arguments.artifacts)
        shutil.rmtree(tmpdir)
        sys.exit(1)
else:
    # Downloading last sucessful build
    filepath = os.path.join(tmpdir, CheckConsts.ARTIFACT_FILE_PATH)
    print 'Downloading {0}.'.format(CheckConsts.LAST_ECLIPSE_REPOSITORY)
    try:
        artifact_file = open(filepath, 'w+b')
        remote_file = urllib2.urlopen(CheckConsts.LAST_ECLIPSE_REPOSITORY)
        shutil.copyfileobj(remote_file, artifact_file)
    except IOError as e:
        print e.strerror
        shutil.rmtree(tmpdir)
        sys.exit(1)
    finally:
        artifact_file.close()
        remote_file.close()
    print 'Successfully downloaded to {0}.'.format(filepath)

# Downloading products
tempproducts = []
if internetproducts:
    tempproducts = [os.path.join(tmpdir, path)
            for path in Const.PRODUCT_ARCHIVE_FILENAMES]
    for i in range(len(tempproducts)):
        print 'Downloading {0} to {1}.'.format(arguments.products[i],
                tempproducts[i])
        if not download(arguments.products[i], tempproducts[i]):
            print 'Unable to downloading {0} to {1}.'.format(arguments.products[i],
                    tempproducts[i])
            shutil.rmtree(tmpdir)
            sys.exit(1)

    # Use downloaded products
    arguments.products = tempproducts
    print 'All products are downloaded.'

# Unzipping artifacts
artifact_zip = zipfile.ZipFile(filepath)
try:
    print 'Unzipping {0} under {1}.'.format(filepath, tmpdir)
    artifact_zip.extractall(tmpdir)
    print 'Unzipped under {0}.'.format(tmpdir)
except IOError as e:
    print e
    shutil.rmtree(tmpdir)
    sys.exit(1)
finally:
    artifact_zip.close()

# Define folder names
nightlypath = os.path.join(tmpdir, Const.NIGHTLY_OUTPUT_DIR)
ldt_nightly_path = '{0}{1}'.format(nightlypath, Const.LDT_SUB_DIRECTORY)
artifact_content = os.path.join(tmpdir, Const.ARTIFACT_FOLDER)

# Creating file tree
try:
    # Creating directories
    for directory in [Const.RELEASE_MILESTONES_DIR, 'products/milestones']:
        dir_to_create = os.path.join(tmpdir, directory)
        os.makedirs(dir_to_create)
        print '{0} created.'.format(dir_to_create)

    # Creating p2 xml
    xmldir = os.path.join(tmpdir, Const.RELEASE_MILESTONES_DIR)
    files = {
        os.path.join(xmldir, Const.COMPOSITE_CONTENT_XML_FILENAME):
            Const.COMPOSITE_CONTENT_XML,
        os.path.join(xmldir, Const.COMPOSITE_ARTIFACTS_XML_FILENAME):
            Const.COMPOSITE_ARTIFACTS_XML}
    for path, content in files.iteritems():
        print 'Creating {0}.'.format(path)
        xmlfile = open(path, 'w')
        xmlfile.write(content)
        xmlfile.close()

    # Copying artifacts under right directories
    print 'Copying artifacts files from {0} to {1}.'.format(artifact_content,
            ldt_nightly_path)
    shutil.copytree(artifact_content, ldt_nightly_path)
    print 'Copy of eclipse release structure available under {0}.'.\
            format(tmpdir)

    # Packing products
    productspath = os.path.join(tmpdir, 'products/current-milestone')
    os.mkdir(productspath)
    print 'Packing products in {0}.'.format(productspath)
    for file in arguments.products:
        if internetproducts:
            shutil.move(file, productspath)
        else:
            shutil.copy(file, productspath)
    print 'Products available at {0}.'.format(productspath)
except OSError as e:
    print 'Unable create test tree, {0}. '.format(e)
    shutil.rmtree(tmpdir)
    sys.exit(1)
finally:
    shutil.rmtree(artifact_content)
    print 'Flushing extracted artifacts at {0}.'.format( artifact_content )
print 'All good.'
