import setuptools

setuptools.setup(
    name="inidiff",
    version="0.1.0",
    url="https://github.com/kragniz/inidiff",

    author="Louis Taylor",
    author_email="louis@kragniz.eu",

    description="Find the differences between two ini config files",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'six',
        'ordered-set'
    ],

    entry_points = {
        'console_scripts': ['inidiff=inidiff:main'],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
