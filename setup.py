from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in bonyan_app/__init__.py
from bonyan_app import __version__ as version

setup(
	name='bonyan_app',
	version=version,
	description='customize in erpnext',
	author='open-alt',
	author_email='erpnext@open-alt.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
