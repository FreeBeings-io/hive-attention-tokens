import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info[0] == 3 and sys.version_info[1] >= 6, "Hive Attention Tokens requires Python 3.6 or newer"

setup(
    name='hive_attention_tokens',
    version='0.0.1',
    description='A protocol for attention tokens on the Hive blockchain.',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['scripts']),
    install_requires=[
        'psycopg2',
    ],
    entry_points = {
        'console_scripts': [
            'hive_attention_tokens = hive_attention_tokens.run_hat:run'
        ]
    }
)