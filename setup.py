#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import scille_core_back

setup(
    name='scille_core_back',
    version=scille_core_back.__version__,
    packages=find_packages(),
    author="SCILLE SAS",
    author_email="tous@scille.fr",
    description="Backend generic of SCILLE SAS",
    long_description=open('README.md').read(),
    install_requires=["pymongo==2.9",
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
                      "gunicorn==19.3.0",  # Application server
                      "xmltodict==0.9.2",
                      "pysolr==3.3.3",
                      "python-dateutil==2.4.2",
                      "python-daemon==2.0.5",
                      "mongopatcher==0.2.5",
                      "suds-jurko==0.6"],
    include_package_data=False,
    url='https://github.com/Scille/xin-back',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 0 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.2",
        "Topic :: Communications",
    ],
    entry_points={
    },
    license="WTFPL",
)
