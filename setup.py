from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Document based light weight database.'
LONG_DESCRIPTION = 'Document based NoSQL light weight database for simple queries and to embed in python application.'

#Setting up
setup(
    name = 'touchdb',
    version=VERSION,
    author = 'Kabilan Mahathevan',
    author_email = '<kabilanen@gmail.com>',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ['json'],
    keywords = ['touchdb', 'python', 'embedded database', 'nosql','document'],
    classifiers = [
        'Development Status :: 1 - Planning', 
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
        ]
)