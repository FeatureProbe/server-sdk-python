# Copyright 2022 FeatureProbe
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

import featureprobe


def _requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [req.strip() for req in f.readlines()]


pypi_classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

if 'a' in featureprobe.__version__:
    pypi_classifiers.append('Development Status :: 3 - Alpha')
elif 'b' in featureprobe.__version__ or 'rc' in featureprobe.__version__:
    pypi_classifiers.append('Development Status :: 4 - Beta')
else:
    pypi_classifiers.append('Development Status :: 5 - Production/Stable')

setup(
    name='featureprobe-server-sdk-python',
    version=featureprobe.__version__,

    author='FeatureProbe',
    license='Apache 2.0',
    license_file='LICENSE',

    description='FeatureProbe Server Side SDK for Python',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    long_description_content_type='text/x-rst',

    keywords=['feature management', 'server sdk'],
    classifiers=pypi_classifiers,

    packages=find_packages(),

    python_requires='>=3.5, <4',
    install_requires=_requirements(),

    project_urls={
        'Project Homepage': 'https://github.com/FeatureProbe',
        'Source Code': 'https://github.com/FeatureProbe/server-sdk-python',
        'Bug Reports': 'https://github.com/FeatureProbe/server-sdk-python/issues',
    }
)
