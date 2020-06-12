import pathlib
from setuptools import setup

# The directory containing this file
LOCAL_PATH = pathlib.Path(__file__).parent

# The text of the README file
README_FILE = (LOCAL_PATH / "README.md").read_text()

# Load requirements, so they are listed in a single place
with open("requirements.txt") as fp:
    install_requires = [dep.strip() for dep in fp.readlines()]

# This call to setup() does all the work
setup(
    name="distfeat",
    version="0.1",  # remember to sync with __init__.py
    description="Library for manipulation of phonological distinctive features",
    long_description=README_FILE,
    long_description_content_type="text/x-markdown",
    url="https://github.com/tresoldi/distfeat",
    #    project_urls = {
    #        "Documentation": "https://dafsa.readthedocs.io",
    #    },
    author="Tiago Tresoldi",
    author_email="tresoldi@shh.mpg.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    packages=["distfeat", "resources"],
    keywords=["distinctive features", "segmental features", "phonology", "phonetics"],
    include_package_data=True,
    install_requires=install_requires,
    entry_points={"console_scripts": ["distfeat=distfeat.__main__:main"]},
    test_suite="tests",
    tests_require=[],
    zip_safe=False,
)
