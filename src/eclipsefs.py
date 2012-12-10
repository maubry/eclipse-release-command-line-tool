# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import tempfile
from os.path import join

class EclipseFS:

    """Representation of build.eclipse.org file system, all needed path are computed here.
    There is no file system operation performed, only the path management is performed here."""

    # List of products name
    PRODUCT_FILENAMES = {'ldt':
                              ['org.eclipse.koneki.ldt.product-linux.gtk.x86_64.tar.gz',
                               'org.eclipse.koneki.ldt.product-macosx.cocoa.x86_64.tar.gz',
                               'org.eclipse.koneki.ldt.product-win32.win32.x86.zip',
                               'org.eclipse.koneki.ldt.product-linux.gtk.x86.tar.gz',
                               'org.eclipse.koneki.ldt.product-win32.win32.x86_64.zip']}
    
    
    # Continuous integration folders
    _CI = 'shared/jobs/koneki-ldt/lastSuccessful/archive/product/target/'
    _CI_PRODUCT = 'products/'
    _CI_REPO = 'repository/'
    
    
    _HOME = 'home/data/httpd/download.eclipse.org/koneki/'
    LDT_SUB_DIRECTORY = 'ldt/'
    _NIGHTLY = 'updates-nightly/{0}'.format(LDT_SUB_DIRECTORY)

    # Release
    _RELEASED_MILESTONES = 'releases/milestones'

    # Current milestone
    _CURRENT_MILESTONE = 'products/current-milestone/'

    _PRODUCT_CURRENT_MILESTONE = 'products/current-milestone/'  

    # Archive
    _ARCHIVE = 'home/data/httpd/archive.eclipse.org/koneki/'
    _ARCHIVE_PRODUCT = '{0}products/milestones/'.format(_ARCHIVE)
    
    # File name constant
    PRODUCT_FILENAMES = ['org.eclipse.koneki.ldt.product-linux.gtk.x86_64.tar.gz',
                    'org.eclipse.koneki.ldt.product-macosx.cocoa.x86_64.tar.gz',
                    'org.eclipse.koneki.ldt.product-win32.win32.x86.zip',
                    'org.eclipse.koneki.ldt.product-linux.gtk.x86.tar.gz',
                    'org.eclipse.koneki.ldt.product-win32.win32.x86_64.zip']
   
    # DOWNLOAD constant
    _DOWNLOAD_ROOT_DIRECTORY = 'home/data/httpd/download.eclipse.org/koneki/'

    _RELEASE_ROOT_PRODUCTS_DIRECTORY = _DOWNLOAD_ROOT_DIRECTORY + 'products/'
    _RELEASE_MILESTONE_PRODUCTS_DIRECTORY = _RELEASE_ROOT_PRODUCTS_DIRECTORY + 'current-milestone/'
    _RELEASE_STABLE_PRODUCTS_DIRECTORY = _RELEASE_ROOT_PRODUCTS_DIRECTORY + 'stable/'

    _RELEASE_ROOT_REPOSITORY = _DOWNLOAD_ROOT_DIRECTORY + 'releases/'
    _RELEASE_STABLE_REPOSITORY = _RELEASE_ROOT_REPOSITORY + 'stable/'
    _RELEASE_MILESTONES_REPOSITORY = _RELEASE_ROOT_REPOSITORY + 'milestones/'
    
    _NIGHTLY_REPOSITORY = _DOWNLOAD_ROOT_DIRECTORY + "updates-nightly/"
    _NIGHTLY_MAINTENANCE_REPOSITORY = _DOWNLOAD_ROOT_DIRECTORY + "updates-nightly-maintenance/"

    # Archive constant
    _ARCHIVE_ROOT_DIRECTORY = 'home/data/httpd/archive.eclipse.org/koneki/'
    
    _ARCHIVE_ROOT_PRODUCTS_DIRECTORY = _ARCHIVE_ROOT_DIRECTORY + 'products/'
    _ARCHIVE_MILESTONES_PRODUCTS_DIRECTORY = _ARCHIVE_ROOT_PRODUCTS_DIRECTORY + 'milestones/'
    _ARCHIVE_STABLE_PRODUCTS_DIRECTORY = _ARCHIVE_ROOT_PRODUCTS_DIRECTORY + 'stable/'
    
    _ARCHIVE_ROOT_REPOSITORY = _ARCHIVE_ROOT_DIRECTORY + 'releases/'
    _ARCHIVE_STABLE_REPOSITORY = _ARCHIVE_ROOT_REPOSITORY + 'stable/'
    _ARCHIVE_MILESTONES_REPOSITORY = _ARCHIVE_ROOT_REPOSITORY + 'milestones/'
    

    def __init__(self, oldversion, newversion, root=None):

        # Remember required versions
        self._old_version = oldversion
        self._new_version = newversion

        # Define the root of the arborescence we are about to create
        self._rootFolder = tempfile.mkdtemp() if root is None else root

        # Continuous integration forlders
        self._ci = join(self.root(), EclipseFS._CI)


