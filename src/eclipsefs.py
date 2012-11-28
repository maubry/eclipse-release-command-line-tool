# vi: sw=4 ts=4 expandtab smarttab ai smartindent
import tempfile
from os.path import join

class EclipseFS:

    """Representation of build.eclipse.org file system, all needed path are computed here.
    There is no file system operation performed, only the path management is performed here."""

    # Continuous integration folders
    _CI          = 'shared/jobs/koneki-ldt/lastSuccessful/archive/product/target/'
    _CI_PRODUCT  = 'products/'
    _CI_REPO    = 'repository/'
    PRODUCT_ARCHIVE_FILENAMES = ['org.eclipse.koneki.ldt.product-linux.gtk.x86_64.tar.gz',
                    'org.eclipse.koneki.ldt.product-macosx.cocoa.x86_64.tar.gz', 
                    'org.eclipse.koneki.ldt.product-win32.win32.x86.zip',
                    'org.eclipse.koneki.ldt.product-linux.gtk.x86.tar.gz',
                    'org.eclipse.koneki.ldt.product-win32.win32.x86_64.zip']
    
    _HOME     = 'home/data/httpd/download.eclipse.org/koneki/'
    LDT_SUB_DIRECTORY = 'ldt/'
    _NIGHTLY = 'updates-nightly/{0}'.format(LDT_SUB_DIRECTORY)

    # Jars
    _ARTIFACTS_JAR = 'artifacts.jar'
    _CONTENT_JAR   = 'content.jar'

    # XML
    COMPOSITE_ARTIFACTS = 'compositeArtifacts.xml'
    COMPOSITE_CONTENT   = 'compositeContent.xml'

    # Release
    _RELEASED_MILESTONES = 'releases/milestones'

    # Current milestone
    _CURRENT_MILESTONE = 'products/current-milestone/'

    _PRODUCT_CURRENT_MILESTONE = 'products/current-milestone/'  

    # Archive
    _ARCHIVE         = 'home/data/httpd/archive.eclipse.org/koneki/'
    _ARCHIVE_PRODUCT = '{0}products/milestones/'.format(_ARCHIVE)

    def __init__(self, oldversion, newversion, root=None):

        # Remember required versions
        self._old_version = oldversion
        self._new_version = newversion

        # Define the root of the arborescence we are about to create
        self._rootFolder = tempfile.mkdtemp() if root is None else root

        # Continuous integration forlders
        self._ci = join(self.root(), EclipseFS._CI)

    def ci(self):
        """Path to continuous integration folder."""
        return self._ci

    def ci_product(self):
        """Path to product continuous integration folder."""
        return join(self.ci(), EclipseFS._CI_PRODUCT)

    def ci_products(self):
        """Path to lastest products from continuous integration."""
        return [join(self.ci_product(), product)
                for product in EclipseFS.PRODUCT_ARCHIVE_FILENAMES]

    def ci_repository(self):
        """Path to lastest continuous integration repository."""
        return join(self.ci(), EclipseFS._CI_REPO)

    def milestones(self):
        """Path to folder containing all milestones."""
        return join(self._home(), EclipseFS._RELEASED_MILESTONES)

    def milestones_composite_artifacts(self):
        """Path to composite artifacts XML file above all milestones."""
        return join(self.milestones(),
                EclipseFS.COMPOSITE_ARTIFACTS)

    def milestones_composite_content(self):
        """Path to composite content XML file above all milestones."""
        return join(self.milestones(),
                EclipseFS.COMPOSITE_CONTENT)

    def milestones_xml_files(self):
        """Path to composite XML files above all milestones."""
        return [self.milestones_composite_content(),
                self.milestones_composite_artifacts()]

    def milestone_composite_artifacts(self):
        """Composite artifacts XML file path for new milestone."""
        return join(self._new_milestone_home(), EclipseFS.COMPOSITE_ARTIFACTS)

    def milestone_composite_content(self):
        """Composite content xml file path for new milestone."""
        return join(self._new_milestone_home(), EclipseFS.COMPOSITE_CONTENT)

    def _home(self):
        """Home of Koneki at download.eclipse.org."""
        return join(self.root(), EclipseFS._HOME)

    def current_milestone(self):
        """Path to products for current milestone."""
        return join(self._home(), EclipseFS._CURRENT_MILESTONE) 

    def new_milestone(self):
        """Path of new milestone to be released."""
        return join(self._new_milestone_home(), EclipseFS.LDT_SUB_DIRECTORY)

    def new_milestone_artifacts(self):
        """Artifacts.jar for new milestone."""
        return join(self.new_milestone(), EclipseFS._ARTIFACTS_JAR)

    def new_milestone_content(self):
        """Content.jar for new milestone."""
        return join(self.new_milestone(), EclipseFS._CONTENT_JAR)

    def _new_milestone_home(self):
        """Root folder of new milestone."""
        return join(self.milestones(), self._new_version)

    def new_milestone_xml_files(self):
        """Path to composite artifacts and content at root of new milestone folder."""
        home = self._new_milestone_home()
        return [join(home, EclipseFS.COMPOSITE_CONTENT),
                join(home, EclipseFS.COMPOSITE_ARTIFACTS)]

    def nightly(self):
        """Nightly update site path."""
        return join(self._home(), EclipseFS._NIGHTLY)

    def nightly_jars(self):
        """Jars contained in nighly directory."""
        nighly = self.nightly()
        return [join(nighly, EclipseFS._ARTIFACTS_JAR),
                join(nighly, EclipseFS._CONTENT_JAR)]

    def _product_archived_milestones(self):
        """Path to folder containing all archived milestone products."""
        return join(self.root(), EclipseFS._ARCHIVE_PRODUCT)

    def product_archive(self):
        """Path to folder where current milestone should be archived,
        it is computed after the `old version` provided at construction."""
        return join(self._product_archived_milestones(), self._old_version)

    def product_current_milestone(self):
        """Path to current milestone folder."""
        return join(self._home(), EclipseFS._PRODUCT_CURRENT_MILESTONE)

    def root(self):
        """Root of current arborescence."""
        return self._rootFolder
