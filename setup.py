import os
from setuptools import setup, find_packages

PACKAGE = "webull"
DESCRIPTION = "Webull Python SDK."
TOPDIR = os.path.dirname(__file__) or "."
VERSION = __import__(PACKAGE).__version__
AUTHOR = "Webull"
AUTHOR_EMAIL = ""
URL = ""
RD_CONTENT_TYPE = "text/markdown"
LICENSE = "Apache License 2.0"

with open("README.rst") as fp:
    LONG_DESCRIPTION = fp.read()

requires = [
    "jmespath>=0.9.3,<1.0.0",
    "cachetools>=5.2.0,<6",
    "paho-mqtt>=1.6.1,<2",
    "urllib3>=2.0",
    "requests>=2.31.0",
    "six>=1.16.0",

    # cryptography
    "cryptography>=3.4,<42; python_version<'3.12'",
    "cryptography>=41.0,<43; python_version>='3.12'",

    # protobuf
    "protobuf>=4.21.12,<5; python_version<'3.12'",
    "protobuf>=4.25.0,<6; python_version>='3.12'",

    # grpc
    "grpcio>=1.51.1,<1.60; python_version<'3.12'",
    "grpcio>=1.60.0,<1.70; python_version>='3.12'"
]

extras_require = {
    "dev": [
        "grpcio-tools>=1.60,<1.70",
    ]
}

setup_args = {
    'python_requires':'>=3.8,<3.14',
    'version': VERSION,
    'author': AUTHOR,
    'author_email': AUTHOR_EMAIL,
    'description': DESCRIPTION,
    'long_description_content_type': RD_CONTENT_TYPE,
    'license': LICENSE,
    'url': URL, 
    'packages': find_packages(exclude=["tests*"]),
    'package_data': {'webull.core': ['data/*.json', '*.pem', "vendored/*.pem"],
                     'webull.core.vendored.requests.packages.certifi': ['cacert.pem']},
    'platforms': 'any',
    'install_requires': requires 
}

setup(name='webull-openapi-python-sdk', **setup_args)