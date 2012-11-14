# vi: sw=4 ts=4 expandtab smarttab ai smartindent
class Const:
    ARCHIVE_MILESTONE            = 'products/milestones/'
    ARCHIVE_PATH                 = '/home/data/httpd/archive.eclipse.org/koneki/'
    ARTIFACT_FILE                = 'artifacts.jar'
    CONTENT_FILE                 = 'content.jar'
    PRODUCT_CURRENT_MILESTONE    = 'products/current-milestone/'
    NIGHTLY_OUTPUT_DIR           = "updates-nightly/"
    LAST_CI_PRODUCTS_PATH        = "/shared/jobs/koneki-ldt/lastSuccessful/archive/product/target/products/"
    LAST_CI_REPOSITORY_PATH      = "/shared/jobs/koneki-ldt/lastSuccessful/archive/product/target/repository/"
    LDT_SUB_DIRECTORY            = 'ldt/'
    ARTIFACT_FILE_PATH           = 'archive.zip'
    RELEASE_MILESTONES_DIR       = 'releases/milestones'
    ARTIFACT_MANIFEST            = 'artifacts.xml'
    ARTIFACT_FOLDER              = 'repository/'
    FOLDER_PERMISSIONS           = 02775
    FILE_PERMISSIONS             = 0664
    LAST_ECLIPSE_REPOSITORY      = 'https://hudson.eclipse.org/hudson/job/koneki-ldt/lastSuccessfulBuild/artifact/product/target/repository/*zip*/repository.zip'
    COMPOSITE_ARTIFACTS_XML_FILENAME = 'compositeArtifacts.xml'
    COMPOSITE_CONTENT_XML_FILENAME   = 'compositeContent.xml'
    PRODUCT_ARCHIVE_FILENAMES    = ['org.eclipse.koneki.ldt.product-linux.gtk.x86_64.tar.gz',
            'org.eclipse.koneki.ldt.product-macosx.cocoa.x86_64.tar.gz', 
            'org.eclipse.koneki.ldt.product-win32.win32.x86.zip',
            'org.eclipse.koneki.ldt.product-linux.gtk.x86.tar.gz',
            'org.eclipse.koneki.ldt.product-win32.win32.x86_64.zip']
