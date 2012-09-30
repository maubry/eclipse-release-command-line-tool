#!/usr/bin/python
# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import argparse
import tempfile
import os
import shutil
import sys
import urllib2
import zipfile
class CheckConsts:
    ARTIFACT_FILE_PATH      = 'archive.zip'
    ARTIFACT_FOLDER         = 'repository/'
    LAST_ECLIPSE_REPOSITORY = 'https://hudson.eclipse.org/hudson/job/koneki-ldt/lastSuccessfulBuild/artifact/product/target/repository/*zip*/repository.zip'
# Creating parsing arguments
parser = argparse.ArgumentParser(description='Create the files properly to run deploy script.')
parser.add_argument('-a', '--artifacts',
    help    = 'Artifacts zip file path',
    metavar = 'artifacts_zip_path',
    nargs   = '?')
arguments = parser.parse_args()
tmpdir = tempfile.mkdtemp()
print 'Everything will happen under temporary folder {0}.'.format(tmpdir)

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

# Unzipping artifacts
artifact_zip = zipfile.ZipFile(filepath)
try:
    print 'Unzipping {0} under {1}.'.format(filepath, tmpdir)
    artifact_zip.extractall(tmpdir)
    print 'Unzipped under {0}.'.format(tmpdir)
except IOError as e:
    print e
    sys.exit(1)
finally:
    artifact_zip.close()

# Creating file tree
try:
    # Creating directories
    dirs = ['releases/milestones', 'products/current-milestone'
        'products/milestones']
    for dir in dirs:
        dir_to_create = os.path.join(tmpdir, dir)
        os.makedirs(dir_to_create)
        print '{0} created.'.format(dir_to_create)

    # Copying artifacts under right directories
    nightly_path = os.path.join(tmpdir, 'nightly')
    artifact_content = os.path.join(tmpdir, CheckConsts.ARTIFACT_FOLDER)
    print 'Copying artifacts files from {0} to {1}.'.format(artifact_content,
        nightly_path)
    shutil.copytree(artifact_content, nightly_path)
    print 'Copy of eclipse release structure available under {0}.'.\
        format(tmpdir)
except OSError as e:
    print 'Unable create test tree, {0}.'.format(e.strerror)
    shutil.rmtree(tmpdir)
    sys.exit(1)
finally:
    shutil.rmtree(artifact_content)
    print 'Flushing extracted artifacts at {0}.'.format( artifact_content )
print 'All good.'
