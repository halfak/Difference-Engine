import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def requirements(fname):
	for line in open(os.path.join(os.path.dirname(__file__), fname)):
		yield line.strip()

setup(
	name = "diffengine",
	version = read('VERSION').strip(),
	author = "Aaron Halfaker",
	author_email = "ahalfaker@wikimedia.org",
	description = ("A difference tracker for MediaWiki."),
	license = "MIT",
	url = "https://github.com/halfak/Difference-Engine",
	py_modules = ['diffengine'],
	long_description = read('README.rst'),
	install_requires = requirements('requirements.txt'),
	classifiers=[
		"Development Status :: 2 - Pre-Alpha",
		"License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
		"Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring"
	],
)
