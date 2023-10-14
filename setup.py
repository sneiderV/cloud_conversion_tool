'''
Setup of the python package for the API 
'''
from setuptools import setup

setup(
    name='conversion_app',
    packages=['conversion_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'marshmallow-sqlalchemy',
        'flask-cors',
        'faker',
        'flask-restful',
        'flask-marshmallow',
        'flask-jwt',
        'flask-jwt-extended',
        'python-dotenv',
        'psycopg2-binary',
        'marshmallow_enum'
    ],
)