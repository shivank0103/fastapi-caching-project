import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='cashifypythoncachingframework',
    version='0.0.1',
    description='Caching framework for Python',
    url='https://github.com/shivank0103/python-caching-project',
    author='Shivank Yadav',
    author_email='shivank0103@gmail.com',
    license='unlicense',
    packages=['caching'],
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[
        'redis==4.3.3',
    ],
    zip_safe=False
)
