from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()
    
setup(
        name='CharNet',
        version='1.2.dev0',
        description='manipulate graphs of characters encounter of some books',
        packages=['charnet',],
        license='GPL2',
        long_description=open('LICENSE').read(),
        install_requires=['numpy','scipy','jinja2',],
)
