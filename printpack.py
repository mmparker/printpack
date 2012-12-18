import os
import subprocess
import glob

# Check for the existence of a "printed" folder
# If it doesn't exist, make it
if not os.path.exists(os.path.join(os.getcwd(), "printed")):
    os.mkdir(os.path.join(os.getcwd(), "printed"))


# Ask the user to identify the PDF file they want to print
Tk().withdraw()
pdfpath = askopenfilename(**{'title': 'Which file contains the forms?'})

# Ask the user for the number of forms to be printed - until I can figure
# out a way to get number of pages from Python, this will have to do
nforms = tkSimpleDialog.askinteger('', 'How many forms are included in this file?', **{'minvalue': 1})


# Using pdftk, reorder the forms to put Section A first, then cover sheet, then Sections B-E, then LTBI testing form
for i in range(nforms):
    subprocess.call(['pdftk', pdfpath, 'cat', '{0}-{1}'.format(3 + 16 * i, 6 + 16 *i),  '{0}-{1}'.format(1 + 16 * i, 2 + 16 *i), '{0}-{1}'.format(7 + 16 * i, 16 + 16 *i), 'output', 'reordered{0}.pdf'.format(i + 1)])

# Using gsprint, print each of the forms in the correct order and groupings
# Get the list of files
formlist = glob.glob('reordered*.pdf')

# Print each
for form in formlist:
    
    subprocess.call(['gsprint', '-dFirstPage=1', '-dLastPage=4', form])
    
    subprocess.call(['gsprint', '-dFirstPage=5', '-dLastPage=14', form])
    
    subprocess.call(['gsprint', '-dFirstPage=15', '-dLastPage=16', form])



