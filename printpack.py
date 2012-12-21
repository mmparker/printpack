"""Print out nearly-complete TBESC participant packets - in order and correctly stapled.

To use from the command line, just type 'python printpack.py'. Inside the
Python interpreter, use 'print_forms()' to get started.

Requires that pdftk, gsprint, and Ghostscript be installed, and that pdftk and
gsprint be on the system path (i.e., you can type in 'pdftk' and 'gsprint' at
the command line to run those programs).

"""

import os
from tempfile import mkdtemp
from Tkinter import Tk
from tkFileDialog import askopenfilename
from ConfigParser import ConfigParser
from ConfigParser import NoOptionError
from subprocess import call
from glob import glob
from shutil import rmtree
import sys

def print_forms():
    """Print TBESC forms in sequence, including pre-enroll and consent.
    
    Using pdftk, reorder the forms to put Section A first, 
    then the cover sheet, then Sections B-E, then LTBI testing form
    Then, using gsprint, print the forms in the correct order and in groupings
    that take advantage of automatic stapling.
    """
    #####################################################
    # Directory setup
    #####################################################
    # Check for the existence of a "printed" folder
    # If it doesn't exist, make it
    printdir = os.path.join(os.getcwd(), 'printed')
    if not os.path.exists(printdir):
        os.mkdir(printdir)

    # Create a temporary directory for working with the (potentially many) PDFs
    scratchdir = mkdtemp()

    #####################################################
    # Get user inputs
    #####################################################
    # Create a config object and read in any existing config
    config = ConfigParser()
    config.read('local.cfg')
    if config.sections() == []:
        config.add_section('formpaths')

    # Check for each of the paths. If any are missing, prompt the user to 
    # provide it
    # Ask the user to identify the location of the pre-enrollment form
    try:
        config.get('formpaths', 'preenroll')
    except NoOptionError: 
        Tk().withdraw()
        config.set('formpaths', 
                   'preenroll', 
                   askopenfilename(**{'title': 'Which file contains your blank pre-enrollment form?'}))

    # Ask the user to identify the location of their adult consent form
    try:
        config.get('formpaths', 'adult_consent')
    except NoOptionError: 
        Tk().withdraw()
        config.set('formpaths', 
                   'adult_consent', 
                   askopenfilename(**{'title': 'Which file contains your English adult consent form?'}))

    # Ask the user to identify the location of their parental permission form
    try:
        config.get('formpaths', 'parental_perm')
    except NoOptionError: 
        Tk().withdraw()
        config.set('formpaths', 
                   'parental_perm', 
                   askopenfilename(**{'title': 'Which file contains your English parental permission form?'}))


    # Ask the user to identify the PDF file they want to print
    pdfpath = askopenfilename(**{'title': 'Which file contains the forms?'})
    
    # Ask the user whether these are adult or pediatric forms
    # Compare inputs to these possibilities
    formtypes = {'Adult': 'Adult', 'adult': 'Adult', 'A': 'Adult', 'a': 'Adult',
                 'Pediatric': 'Pediatric', 'pediatric': 'Pediatric',
                 'ped': 'Pediatric', 'Ped': 'Pediatric',
                 'P': 'Pediatric', 'p': 'Pediatric'}

    formtype_input = raw_input('Are these adult or pediatric forms?  ')
    
    try:
        formtype = formtypes[formtype_input]
    except KeyError:
        formtype_input = raw_input("Please type either 'Adult' or 'Pediatric':  ")

    try: 
        formtype = formtypes[formtype_input]
    except KeyError:
        print("Something's still not right. Please try again.")
        sys.exit()

    # Ask the user for the number of forms to be printed - until I can figure
    # out a way to get number of pages from Python, this will have to do
    nforms_input = raw_input('How many forms are in the combined PDF?  ')

    try:
        nforms = int(nforms_input)
    except ValueError:
        nforms_input = raw_input(nforms_input + " isn't an integer. Please try again:  ")

    try:
        nforms = int(nforms_input)
    except ValueError:
        print("Something's still not right. Please try again.")
        sys.exit()


    #####################################################
    # Save the form paths to the config file
    #####################################################
    with open('local.cfg', 'wb') as configfile:
        config.write(configfile)


    #####################################################
    # Call the appropriate subroutine, adult or pediatric
    #####################################################
    if formtype == 'Adult':
        print_adult(pdfpath, nforms, scratchdir, config)
    elif formtype == 'Pediatric':
        print_ped(pdfpath, nforms, scratchdir, config)
    else:
        raise ValueError("Invalid form type - must be 'Adult' or 'Pediatric'")
    
    #####################################################
    # Clean up
    #####################################################
    # Delete the temporary directory
    rmtree(scratchdir)

    # Move the original file into the printed folder
    os.rename(pdfpath, os.path.join(printdir, os.path.split(pdfpath)[1]))


def print_adult(pdfpath, nforms, scratchdir, config):
    """Print adult TBESC forms - use print_forms() instead."""
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
        call(['gsprint', config.get('formpaths', 'preenroll')])
        call(['gsprint', config.get('formpaths', 'adult_consent')])
        call(['gsprint', '-dFirstPage=1', '-dLastPage=4', form])
        call(['gsprint', '-dFirstPage=5', '-dLastPage=14', form])
        call(['gsprint', '-dFirstPage=15', '-dLastPage=16', form])



def print_ped(pdfpath, nforms, scratchdir, config):
    """Print pediatric TBESC forms - use print_forms() instead."""
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
        call(['gsprint', config.get('formpaths', 'preenroll')])
        call(['gsprint', config.get('formpaths', 'parental_perm')])
        call(['gsprint', '-dFirstPage=1', '-dLastPage=4', form])
        call(['gsprint', '-dFirstPage=5', '-dLastPage=13', form])
        call(['gsprint', '-dFirstPage=14', '-dLastPage=15', form])



if __name__ == "__main__":
    print_forms()
