import os
import sys
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
 

def _write_file( path, text ):
    """Writes file containing text to path
    Parameters
    ----------
    path : string 
        Full path containing location & filename of txt file    
    text : string 
        text to be written to file
    """
    _clear_text( path )
    with open( path, "a", encoding="utf-8") as text_file:
       text_file.writelines(text)

#clear_text function
def _clear_text( path ):
    """Creates empty file"""
    open( path, "w" ).close()
   
#writelines function
def writelines(self, lines):
    """Writes lines to file"""
    self._checkClosed()
    for line in lines:
       self.write(line)

#PDF to text Function. 
def pdf_to_text(path):
    """Returns text of pdf

    Parameters
    ----------
    path : string 
        Full path containing location & filename of pdf file

    Returns
    -------
    text : string
        Text from the document    
    """
    manager     = PDFResourceManager()
    retstr      = BytesIO()
    layout      = LAParams(all_texts=True)
    device      = TextConverter(manager, retstr, laparams=layout)
    filepath    = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    filepath.close()
    device.close()
    retstr.close()
    # Convert bytes to string
    text = text.decode("utf-8")
    return text

def pdf_to_text_file( *args ):
    """Converts pdf to text files

    Parameters
    ----------
    args : string 
        Full path containing location & filename of pdf file, or directory containing pdf files

    Returns
    ------- 
    filenames : list
        List of converted file paths
    """
    filenames = []
    for path in args:
        if os.path.isfile( path ):
            # If file, convert to text & write to file
            text = pdf_to_text( path )
            names_out = path.replace( ".pdf", ".txt" ) # write to same directory
            _write_file( names_out, text )
            filenames.append( names_out )
        elif os.path.isdir( path) :
            # If path, recurse
            names_in = filter( lambda x: x.endswith('.pdf'), os.listdir( path ) )
            names_out = pdf_to_text_file( *( os.path.join( path, n ) for n in names_in ) )
            filenames.extend( names_out ) 
        else:
            raise Exception( 'Invalid path [{}]'.format(path) )        
    return filenames
