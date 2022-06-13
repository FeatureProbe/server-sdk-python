import os.path
import pathlib
import re

from setuptools import setup, find_packages

ROOT = pathlib.Path(__file__).parent.resolve()


def get_version():
    with open(os.path.join(ROOT, 'featureprobe', '__init__.py')) as f:
        return re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='featureprobe-server',

    version=get_version(),

    description='FeatureProbe Server Side SDK for Python',

    long_description=(ROOT / 'README.md').read_text(encoding='utf-8'),

    long_description_content_type='text/markdown',

    author='FeatureProbe',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: Apache-2.0',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='feature management, server sdk',

    package_dir={'': 'featureprobe'},
    packages=find_packages(where='featureprobe'),

    python_requires='>=3.8, <4',

    install_requires=[],
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    project_urls={
        'Bug Reports': 'https://github.com/FeatureProbe/server-sdk-python/issues',
        'Source': 'https://github.com/FeatureProbe/server-sdk-python',
    },
)
