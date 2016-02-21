# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages


REQUIRES = (
    "pymongo==2.9",
    "simplejson==3.7.3",
    "Flask==0.10.1",
    "Flask-Cache==0.13.1",
    "Flask-restful==0.3.4",
    "flask-mongoengine==0.7.4",
    "mongoengine==0.10.1",
    "Flask-Principal==0.4.0",
    "Flask-Script==2.0.5",
    "Flask-Cors==2.0.0",
    "Flask-Mail==0.9.1",
    "flask-marshmallow==0.6.0",
    "marshmallow==2.1.1",
    "marshmallow-mongoengine==0.7.0",
    "PyJWT==1.1.0",
    "passlib==1.6.2",
    "Authomatic==0.0.13",
    "requests==2.9.1",
    "docopt==0.6.2",
    "pysolr==3.3.3",
    "python-dateutil==2.4.2",
    "python-daemon==2.0.5",
    "mongopatcher==0.2.5",
)


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version('xin/__init__.py')


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='xin-back',
    version=__version__,
    # description='',
    long_description=read('README.rst'),
    author='Scille',
    author_email='contact@scille.fr',
    url='https://github.com/Scille/xin-back',
    packages=find_packages(exclude=("test*", )),
    package_dir={'xin': 'xin'},
    include_package_data=True,
    install_requires=REQUIRES,
    license='MIT',
    zip_safe=False,
    # keywords='',
    classifiers=[
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
