
# Define the form-printing functions
# Using the path of the PDF of files (pdfpath),
# the type of form ('Adult' or 'Pediatric' - formtype),
# and the number of forms in the file (nforms),
# print complete packets including the static pre-enrollment and the
# English long-form consent or parental permission

import os
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkSimpleDialog import askinteger
from subprocess import call
from glob import glob
from tempfile import mkdtemp
from shutil import rmtree

def print_forms():
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
    #####################################################
    # Directory setup
    #####################################################
    # Check for the existence of a "printed" folder
    # If it doesn't exist, make it
    printdir = os.path.join(os.getcwd(), 'printed');
    if not os.path.exists(printdir):
        os.mkdir(printdir)

    # Create a temporary directory for working with the (potentially many) PDFs
    scratchdir = mkdtemp()

    #####################################################
    # Get user inputs
    #####################################################
    # Ask the user to identify the PDF file they want to print
    Tk().withdraw()
    pdfpath = askopenfilename(**{'title': 'Which file contains the forms?'})
    
    # Ask the user whether these are adult or pediatric forms
    formtype = "Pediatric"
    
    # Ask the user for the number of forms to be printed - until I can figure
    # out a way to get number of pages from Python, this will have to do
    nforms = askinteger('', 
                        'How many forms are included in this file?', 
                        **{'minvalue': 1})
    
    #####################################################
    # Call the appropriate subroutine, adult or pediatric
    #####################################################
    if formtype == 'Adult':
        print_adult(pdfpath, nforms, scratchdir)
    elif formtype == 'Pediatric':
        print_ped(pdfpath, nforms, scratchdir)
    else:
        raise ValueError("Invalid form type - must be 'Adult' or 'Pediatric'")
    
    #####################################################
    # Clean up
    #####################################################
    # Delete the temporary directory
    rmtree(scratchdir)

    # Move the original file into the printed folder
    os.rename(pdfpath, os.path.join(printdir, os.path.split(pdfpath)[1]))


def print_adult(pdfpath, nforms, scratchdir):
    """Print adult TBESC forms - use printforms()."""
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



def print_ped(pdfpath, nforms, scratchdir):
    """Print pediatric TBESC forms - use printforms()."""
    # Loop over the forms, exploding and recombining them
    for i in range(nforms):
        call(['pdftk', pdfpath, 'cat', 
              '{0}-{1}'.format(3 + 15 * i, 6 + 15 *i),  
              '{0}-{1}'.format(1 + 15 * i, 2 + 15 *i), 
              '{0}-{1}'.format(7 + 15 * i, 15 + 15 *i), 
              'output', 
              os.path.join(scratchdir, 'reordered{0}.pdf'.format(i + 1))])
    
    # Using gsprint, print each of the forms in the correct order and groupings
    # First, get the list of reordered files
    formlist = glob(os.path.join(scratchdir, 'reordered*.pdf'))
    
    # Then print each
    for form in formlist:
        call(['gsprint', '-dFirstPage=1', '-dLastPage=4', form])
        call(['gsprint', '-dFirstPage=5', '-dLastPage=13', form])
        call(['gsprint', '-dFirstPage=14', '-dLastPage=15', form])

