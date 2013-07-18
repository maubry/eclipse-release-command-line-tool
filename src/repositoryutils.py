'''
 Utility functions to handle repository
'''
import os
from xml.etree import ElementTree
import StringIO
import time
import zipfile
import shutil

#
#  Repository constants
#############################################

_REPOSITORY_PLUGINS_DIR = "plugins"
_REPOSITORY_ARTIFACTS_XMLFILE = 'artifacts.xml'
_REPOSITORY_CONTENT_XMLFILE = 'content.xml'

_REPOSITORY_ARTIFACTS_JARFILE = 'artifacts.jar'
_REPOSITORY_CONTENT_JARFILE = 'content.jar'

_COMPOSITE_REPOSITORY_ARTIFACTS_FILE = 'compositeArtifacts.xml'
_COMPOSITE_REPOSITORY_CONTENT_FILE = 'compositeContent.xml'
    
_STATS_URI = 'http://download.eclipse.org/stats/koneki'
_LDT_FEATURE_ID = 'org.eclipse.koneki.ldt'

_FOLDER_PERMISSIONS = 02775
_FILE_PERMISSIONS = 0664

#
#  Public Repository Handling function
#############################################

def is_repository(path):
    if os.path.exists(path) and os.path.isdir(path):
        contain_artifact = False
        contain_content = False
        contain_plugins = False
        for f in os.listdir(path):
            if _REPOSITORY_ARTIFACTS_JARFILE == f and os.path.isfile(os.path.join(path,f)):
                contain_artifact = True
            if _REPOSITORY_CONTENT_JARFILE == f and os.path.isfile(os.path.join(path,f)):
                contain_content = True
            if _REPOSITORY_PLUGINS_DIR == f and os.path.isdir(os.path.join(path,f)):
                contain_plugins = True
        return contain_artifact and contain_content and contain_plugins
    return False

def is_composite_repository(path):
    if os.path.exists(path) and os.path.isdir(path):
        contain_artifact = False
        contain_content = False
        for f in os.listdir(path):
            if _COMPOSITE_REPOSITORY_ARTIFACTS_FILE == f and os.path.isfile(os.path.join(path,f)):
                contain_artifact = True
            if _COMPOSITE_REPOSITORY_CONTENT_FILE == f and os.path.isfile(os.path.join(path,f)):
                contain_content = True
        return contain_artifact and contain_content
    return False

def composite_repository_contains(path,child_repository_name):
    child_repository_path = os.path.join(path,child_repository_name)
    if os.path.exists(child_repository_path) and os.path.isdir(child_repository_path):
        return True

def composite_repository_list_child(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))]            

def move_child_from_composite_repository (source_composite_repository_path, destination_composite_repository_path, old_child_repository_name,new_child_repository_name):
    # remove from composite repository files (artifacts and content)
    _xml_remove_child_from_composite_repository(source_composite_repository_path, old_child_repository_name)
    
    # add to composite repository files (artifacts and content)
    _xml_add_child_to_composite_repository(destination_composite_repository_path, new_child_repository_name)
    
    # move folder on file system
    source_path = os.path.join(source_composite_repository_path, old_child_repository_name)
    destination_path = os.path.join(destination_composite_repository_path, new_child_repository_name)
    shutil.move(source_path, destination_path)
    
    # check repository right
    _set_file_permissions(destination_path)

def remove_child_from_composite_repository (composite_repository_path, child_repository_name):
    # remove from composite repository files (artifacts and content)
    _xml_remove_child_from_composite_repository(composite_repository_path, child_repository_name)
    
    # remove folder on file system
    shutil.rmtree(os.path.join(composite_repository_path, child_repository_name))

def add_child_to_composite_repository(composite_repository_path, child_repository_name, child_repository_path):
    # remove from composite repository files (artifacts and content)
    _xml_add_child_to_composite_repository(composite_repository_path, child_repository_name)
    
    # copy folder on file system
    destination_path = os.path.join(composite_repository_path, child_repository_name)
    shutil.copytree(child_repository_path, destination_path)
    
    # check repository right
    _set_file_permissions(destination_path)

def activate_stats(composite_repository_path,stats_uri,feature_ids):
    # activate stats for given repository
    artifacts_file_path = os.path.join(composite_repository_path, _REPOSITORY_ARTIFACTS_JARFILE)
    _xml_zip_activate_stats(artifacts_file_path, _REPOSITORY_ARTIFACTS_XMLFILE, stats_uri, feature_ids)

#
#  Private Repository Handling function
#############################################

def _set_file_permissions(repository_path):
    os.chmod(repository_path, _FOLDER_PERMISSIONS)
    for root, dirs, files in os.walk(repository_path):
        for d in dirs:  
            os.chmod(os.path.join(root,d), _FOLDER_PERMISSIONS)
        for f in files:
            os.chmod(os.path.join(root,f), _FILE_PERMISSIONS)


def _xml_remove_child_from_composite_repository(composite_repository_path, child_repository_name):
    # remove child from artifacts file
    composite_artifacts_file_path = os.path.join(composite_repository_path, _COMPOSITE_REPOSITORY_ARTIFACTS_FILE)
    _xml_remove_child_repository(composite_artifacts_file_path, child_repository_name)
    _xml_update_p2timestamp(composite_artifacts_file_path)
    
    # remove child from content file
    composite_content_file_path = os.path.join(composite_repository_path, _COMPOSITE_REPOSITORY_CONTENT_FILE)
    _xml_remove_child_repository(composite_content_file_path, child_repository_name)
    _xml_update_p2timestamp(composite_content_file_path)

def _xml_add_child_to_composite_repository(composite_repository_path, child_repository_name):
    # remove child from artifacts file
    composite_artifacts_file_path = os.path.join(composite_repository_path, _COMPOSITE_REPOSITORY_ARTIFACTS_FILE)
    _xml_add_child_repository(composite_artifacts_file_path, child_repository_name)
    _xml_update_p2timestamp(composite_artifacts_file_path)
    
    # remove child from content file
    composite_content_file_path = os.path.join(composite_repository_path, _COMPOSITE_REPOSITORY_CONTENT_FILE)
    _xml_add_child_repository(composite_content_file_path, child_repository_name)
    _xml_update_p2timestamp(composite_content_file_path)
    

#
#  Private XML Handling function
#############################################

def _xml_update_p2timestamp(xml_file_path):
    def f(root):
        # Update properties node
        for properties in root.findall('./properties'):
            # remove child with the given name
            for prop in properties:
                if prop.attrib['name'] == 'p2.timestamp':
                    prop.attrib['value'] = str(long(time.time()))
            
    _xml_handle_file(xml_file_path, f)
    
def _xml_remove_child_repository(xml_file_path, child_repository_name):
    def f(root):
        # Update children node
        for children in root.findall('./children'):
            # remove child with the given name
            for child in children:
                if child.attrib['location'] == child_repository_name:
                    children.remove(child)
            # Update child count
            children.set('size', str(len(children)))
            
    _xml_handle_file(xml_file_path, f)

def _xml_add_child_repository(xml_file_path, child_repository_name):
    def f(root):
        # check if the child is not already present
        need_to_add = True 
        for children in root.findall('./children'):
            for child in children:
                if child.attrib['location'] == child_repository_name:
                    need_to_add = False
                    
        # Update children node
        if need_to_add:
            for children in root.findall('./children'):
                # Append child node
                ElementTree.SubElement(children, 'child', {'location' : child_repository_name})
                # Update child count
                children.set('size', str(len(children)))
            
    _xml_handle_file(xml_file_path, f)
    
    
def _xml_zip_activate_stats(zip_file_path, xml_file_path, stats_uri_value, feature_ids):
    
    def f(root):
        """Add statistics values to artifact xml."""
        isvaluesetted = False
        isstatpropertyset = False
    
        # Adding 'p2.statsURI' to repository properties
        for properties in root.findall('./properties'):
            # Check if an existing node desn't already exist to avoid duplicate it
            for propertie in properties.findall("./property"):
                if propertie.attrib['name'] == 'p2.statsURI' and propertie.attrib['value'] == stats_uri_value:
                    isstatpropertyset = True
            # add the property
            if not isstatpropertyset:
                ElementTree.SubElement(properties, 'property', {
                    'name'  : 'p2.statsURI',
                    'value' : stats_uri_value})
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
            for feature_id in feature_ids:
                if artifact.get('classifier') == 'org.eclipse.update.feature' and \
                        artifact.get('id') == feature_id:
                    version = artifact.get('version')
                    for properties in artifact.findall('./properties'):
                        ElementTree.SubElement(properties, 'property', {
                            'name'  : 'download.stats',
                            'value' : (feature_id + '_{0}').format(version)})
                        properties.set('size', str(len(properties)))
                        isvaluesetted = True
    
        # Notify in case of error
        if not isvaluesetted:
            raise ValueError('Unable to set "download.stats".')
        
    _xml_zip_handle_file(zip_file_path,xml_file_path, f)

def _xml_handle_file(xml_file_path, handlexml_function):
    # load content
    ###############
    xmlfile = open(xml_file_path)
    xml = xmlfile.read()
    xmlfile.close()
    
    # update content
    ################
    # Load XML tree
    root = ElementTree.fromstring(xml)
    # Handle xml
    handlexml_function(root)
    # Return resulting XML as a string
    buf = StringIO.StringIO()
    ElementTree.ElementTree(root).write(buf)
    xml = buf.getvalue()
    buf.close()
    
    # save content
    ################
    xmlfile = open(xml_file_path, 'w')
    xmlfile.write(xml)
    xmlfile.close()

def _xml_zip_handle_file(zip_file_path, xml_file_path, handlexml_function):
    # load content
    ###############
    zfile = zipfile.ZipFile(zip_file_path)
    xml = zfile.read(xml_file_path)
    zfile.close()

    # update content
    ################           
    # Load XML tree
    root = ElementTree.fromstring(xml)
    # Handle xml
    handlexml_function(root)
    # Return resulting XML as a string
    buf = StringIO.StringIO()
    ElementTree.ElementTree(root).write(buf)
    xml = buf.getvalue()
    buf.close()
    
    # save content
    ################
    zfile = zipfile.ZipFile(zip_file_path, 'w')
    zfile.writestr(xml_file_path,
            xml)
    zfile.close

    
