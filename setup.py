#! /usr/bin/env python
#
# Copyright 2020 Peter Dowell <p.g.dowell@gmail.com>

#Define constants
DISTNAME="summarise"
MAINTAINER="Peter Dowell"
MAINTAINER_EMAIL="p.g.dowell@gmail.com"
DESCRIPTION="Summarise speeches contained in .pdf documents."
LICENSE=""
URL="https://github.com/condensedWeasel/speech-nlp"
NUMPY_MIN_VERSION=""
PANDAS_MIN_VERSION=""

import os, sys, re

# Get description from README.md
readme = os.path.join( os.path.dirname(__file__),"README.md" )
LONG_DESCRIPTION = open( readme ).read()

# Version number is contained in package
VERSION = get_version()

def setup_package():
    """ Sets up package metadata """
    from setuptools import setup, find_packages

    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    long_description=LONG_DESCRIPTION,
                    license=LICENSE,
                    url=URL,                    
                    version=VERSION,                    
                    classifiers=['Intended Audience :: Science/Research',
                                 'Intended Audience :: Developers',
                                 'Programming Language :: Python',
                                 'Topic :: Software Development',
                                 'Topic :: Scientific/Engineering',
                                 'Operating System :: Microsoft :: Windows', 				                 
                                 'Programming Language :: Python :: 3.7',
                                 'Programming Language :: Python :: 3.8'
                                 ],                   
                    python_requires=">=3.7",
                    install_requires=[
                        'numpy>={}'.format(NUMPY_MIN_VERSION),
                        'pandas>={}'.format(PANDAS_MIN_VERSION)
                        ],
		            )
    metadata['packages'] = find_packages()
    setup(**metadata)

def get_version():
    version_re = re.compile("""__version__[\s]*=[\s]*['|"](.*)['|"]""")
    init_file = os.path.join( os.path.dirname(__file__), DISTNAME, "__init__.py" )
    with open(init_file) as file:
        content = file.read()
        match = version_re.search(content)
        version = match.group(1)
    return version

if __name__ == "__main__":
    setup_package()