from setuptools import setup

setup(
    name='x5gon_rest_api',
    version='0.1',
    packages=['test', 'x5gon_rest', 'x5gon_rest.api', 'x5gon_rest._data', 'x5gon_rest.utils',
              'x5gon_rest.models'],
    url='www.x5gon.org',
    license='',
    author='',
    description='The API implementation for x5db Duplicate detection and language detection',
    install_requires=[
        'Flask==1.1.2',
        'gunicorn==20.0.4',
        'Werkzeug==1.0.1',
        'fasttext==0.9.2',
        'psycopg2==2.8.6',
        'requests==2.24.0',
        'tqdm==4.50.0',
        'flask-restplus==0.13.0'
    ]
)
