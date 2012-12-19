
from subprocess import call
from glob import glob
from tempfile import mkdtemp
from shutil import rmtree

# Define the form-printing function
# Using the path of the PDF of files (pdfpath),
# the type of form ('Adult' or 'Pediatric' - formtype),
# and the number of forms in the file (nforms),
# print complete packets including the static pre-enrollment and the
# English long-form consent or parental permission

def printforms(pdfpath, formtype, nforms):
    """Print TBESC forms in sequence, including pre-enroll and consent.
    
    Using pdftk, reorder the forms to put Section A first, 
    then the cover sheet, then Sections B-E, then LTBI testing form
    Then, using gsprint, print the forms in the correct order and in groupings
    that take advantage of automatic stapling.

    Args:
    pdfpath: the path to the PDF containing the combined forms
    formtype: whether the forms are 'Adult' or 'Pediatric'
    nforms: how many forms are contained in the file

    """
    # Create a temporary directory for working with the (potentially many) PDFs
    scratchdir = mkdtemp()

    # Loop over the forms, exploding and recombining them
    for i in range(nforms):
        call(['pdftk', pdfpath, 'cat', 
              '{0}-{1}'.format(3 + 16 * i, 6 + 16 *i),  
              '{0}-{1}'.format(1 + 16 * i, 2 + 16 *i), 
              '{0}-{1}'.format(7 + 16 * i, 16 + 16 *i), 
              'output', 
              os.path.join(scratchdir, 'reordered{0}.pdf'.format(i + 1))])
    
    # Using gsprint, print each of the forms in the correct order and groupings
    # First, get the list of reordered files
    formlist = glob(os.path.join(scratchdir, 'reordered*.pdf'))
    
    # Then print each
    for form in formlist:
        call(['gsprint', '-dFirstPage=1', '-dLastPage=4', form])
        call(['gsprint', '-dFirstPage=5', '-dLastPage=14', form])
        call(['gsprint', '-dFirstPage=15', '-dLastPage=16', form])
    
    # Delete the temporary directory
    rmtree(scratchdir)

