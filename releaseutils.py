# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import os
import sys
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
    for artifact in root.findall('./artifacts/artifact[@id="org.eclipse.koneki.ldt"]'):
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

def checkpermissions(parent_folder, files):
	# Checking parent directory
	sys.stdout.write('Setting permissions on {0}: '.format(parent_folder))
	try:
		os.chmod(parent_folder, 02765)
		sys.stdout.write('Done\n')
	except OSError as ex:
		sys.stdout.write('Error.\nUnable to set permissions on {0}.\n{1}'\
				.format(parent_folder, ex.message))
		return False

	# Checking children
	for file in files:
		try:
			sys.stdout.write('Setting permissions on {0}: '.format(file))
			os.chmod(file, 0664)
			sys.stdout.write('Done\n')
		except OSError as e:
			sys.stdout.write('Error\nUnable to set permissions on {0}.\n{1}'\
					.format(file, e.strerror))
			return False
	return True
