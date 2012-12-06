import os
import subprocess


# Check for the existence of a "printed" folder
# If it doesn't exist, make it
if not os.path.exists(os.path.join(os.getcwd(), "printed")):
    os.mkdir(os.path.join(os.getcwd(), "printed"))


# Ask the user to identify the PDF file they want to print
pdfpath = 'test.pdf'

# Ask the user for the number of forms to be printed - until I can figure
# out a way to get number of pages from Python, this will have to do
# Placeholder for asking
nforms = 5;


# Using gsprint, print each of the forms in correct order
for i in range(nforms):

    subprocess.call(['gsprint', '-dFirstPage={0}'.format(1 + 16 * i), '-dLastPage={0}'.format(2 + 16 * i), pdfpath])
    
    subprocess.call(['gsprint', '-dFirstPage={0}'.format(3 + 16 * i), '-dLastPage={0}'.format(6 + 16 * i), pdfpath])
    
    subprocess.call(['gsprint', '-dFirstPage={0}'.format(7 + 16 * i), '-dLastPage={0}'.format(14 + 16 * i), pdfpath])
    
    subprocess.call(['gsprint', '-dFirstPage={0}'.format(15 + 16 * i), '-dLastPage={0}'.format(16 + 16 * i), pdfpath])


