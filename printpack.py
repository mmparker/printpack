import os
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkSimpleDialog import askinteger


# Check for the existence of a "printed" folder
# If it doesn't exist, make it
printdir = os.path.join(os.getcwd(), 'printed');
if not os.path.exists(printdir):
    os.mkdir(printdir)


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




# Move the original file into the printed folder
os.rename(pdfpath, os.path.join(printdir, os.path.split(pdfpath)[1]))
