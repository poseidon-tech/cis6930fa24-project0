from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Prajay Yalamanchili',
	author_email='yalamanchili.p@ufl.edu',
	packages=find_packages(exclude=('tests', 'docs', 'resources')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)