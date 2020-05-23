import os
from summarise.io import pdf_to_text
from summarise.io import pdf_to_text_file


root = os.path.dirname(__file__)

text = pdf_to_text( os.path.join( root, 'resources', 'samples', 'Document2.pdf' ) )

print( text )

filenames = pdf_to_text_file( os.path.join( root, 'resources', 'samples' ) )

print(filenames)

#filenames = pdf_to_text_file( os.path.join( root, '..', 'data') )