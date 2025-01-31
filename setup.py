from setuptools import setup, find_packages

with open(file='README.md') as f:
    readme = f.read()

setup(
    name='cnv_apps_utilities',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    ],
    author='Benjamin Freyter',
    author_email='benjaminmaciej.freyter@usb.ch',
    description='Utilities for CNV apps',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/neuropathbasel-pub/CNV_apps_utilities',
    classifiers=[
        'Development Status :: 5 - Beta',
        'Intended Audience :: Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Ubuntu 22.04',
    ],
    python_requires='>=3.11',
)