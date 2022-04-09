import os.path
import re
from setuptools import setup

(__version__, ) = re.findall("__version__.*\s*=\s*[']([^']+)[']",
                             open('dcimm/__init__.py').read())

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="dcimm",
    version=__version__,
    description="Digital Camera IMages Management",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/d10xa/dcimm",
    author="Andrey Stolyarov",
    author_email="d10xa@mail.ru",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["dcimm"],
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["dcimm=dcimm.__main__:main"]},
)