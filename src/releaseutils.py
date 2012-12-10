# vi: sw=4 ts=4 expandtab smarttab ai smartindent
from   consts import Const
import os
import StringIO
import sys
import time
import xml.etree.ElementTree as ElementTree
def activatestats(xmlstring, openresultfile):
    """Add statistics values to artifact xml."""

    # Parse xml
    root = ElementTree.fromstring(xmlstring)
    isvaluesetted = False

    # Adding 'p2.statsURI' to repository properties
    for properties in root.findall('./properties'):
        ElementTree.SubElement(properties, 'property',{
            'name'  : 'p2.statsURI',
            'value' : 'http://download.eclipse.org/stats/koneki'})
        properties.set('size', str(len(properties)))
        isvaluesetted = True

    # Notify in case of error
    if not isvaluesetted:
        raise ValueError('Unable to set "p2.statsURI".')
    else:
        isvaluesetted = False

    # Adding 'download.stats' to artifact 'org.eclipse.koneki.ldt'
    for artifact in root.findall('./artifacts/artifact'):

        # Activating stat only on feature
        if artifact.get('classifier') == 'org.eclipse.update.feature' and \
                artifact.get('id') == 'org.eclipse.koneki.ldt':
            version = artifact.get('version')
            for properties in artifact.findall('./properties'):
                ElementTree.SubElement(properties, 'property',{
                    'name'  : 'download.stats',
                    'value' : 'org.eclipse.koneki.ldt_{0}'.format(version)})
                properties.set('size', str(len(properties)))
                isvaluesetted = True

    # Notify in case of error
    if not isvaluesetted:
        raise ValueError('Unable to set "download.stats".')

    # Write successful content
    ElementTree.ElementTree(root).write(openresultfile)

def addxmlchild(xmlstring, childlocation):
    """Add a `children` node in provided xml under '/children',
    also updates children count."""

    # Load XML tree
    root = ElementTree.fromstring(xmlstring)

    # Update children node
    for children in root.findall('./children'):

        # Append child node
        ElementTree.SubElement(children, 'child', {'location' : childlocation})

        # Update child count
        children.set('size', str(len(children)))

    # Return resulting XML as a string
    buffer = StringIO.StringIO()
    ElementTree.ElementTree(root).write(buffer)
    string = buffer.getvalue()
    buffer.close()
    return string

def applydirpermisions(folder):
    sys.stdout.write('Setting permissions on {0}: '.format(folder))
    try:
        os.chmod(folder, Const.FOLDER_PERMISSIONS)
        sys.stdout.write('Done\n')
    except OSError as ex:
        sys.stdout.write('Error.\nUnable to set permissions on {0}.\n{1}'\
                .format(folder, ex.message))
        return False
    return True

def checkpermissions(parent_folder, files):
    for root, dirs, files in os.walk(parent_folder):
        # Checking parent directory
        if not applydirpermisions(root):
            return False
        for dir in dirs:
            if not applydirpermisions(os.path.join(root, dir)):
                return False

        # Checking children
        for file in files:
            try:
                fileabsolutename = os.path.join(root, file)
                os.chmod(fileabsolutename, Const.FILE_PERMISSIONS)
            except OSError as e:
                sys.stdout.write('Error\nUnable to set permissions on {0}.\n{1}'\
                        .format(file, e.strerror))
                return False
    return True

def compositeartifactsxml(version='', times=str(long(time.time()))):
    return """<?xml version='1.0' encoding='UTF-8'?>
    <?compositeArtifactRepository version='1.0.0'?>
    <repository name='Eclipse Koneki Update Site {0}'
            type='org.eclipse.equinox.internal.p2.artifact.repository.CompositeArtifactRepository'
            version='1.0.0'>
        <properties size='1'>
            <property name='p2.timestamp' value='{1}'/>
        </properties>
        <children size='0'></children>
    </repository>""".format(version, times)

def compositecontentxml(version='', times=str(long(time.time()))):
    return  """<?xml version='1.0' encoding='UTF-8'?>
    <?compositeMetadataRepository version='1.0.0'?>
    <repository name='Eclipse Koneki Update Site {0}'
            type='org.eclipse.equinox.internal.p2.metadata.repository.CompositeMetadataRepository'
            version='1.0.0'>
    <properties size='1'>
        <property name='p2.timestamp' value='{1}'/>
    </properties>
    <children size='0'></children>
    </repository>""".format(version, times)
    



def contains_products(products_dir_path, product_filenames):
    if os.path.exists(products_dir_path) and os.path.isdir(products_dir_path):
        files_list = os.listdir(products_dir_path)
        for f in files_list:
            if not (os.path.basename(f) in product_filenames):
                return False
        if len(files_list) !=  len (product_filenames):
            return False
        return True
    return False


