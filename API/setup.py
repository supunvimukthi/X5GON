from setuptools import setup

setup(
    name='x5gon_rest_api',
    version='0.1',
    packages=['test', 'x5gon_rest', 'x5gon_rest.api', 'x5gon_rest._data', 'x5gon_rest.utils',
              'x5gon_rest.models'],
    url='www.x5gon.org',
    license='',
    author='Supun Ranawaka',
    description='The API implementation for x5db Duplicate detection and language detection',
    install_requires=[
        'Flask>=1.0.2',
        'gunicorn>=19.9.0',
        'werkzeug',
        'fasttext',
        'psycopg2',
        'requests',
        'tqdm'
    ]
)
