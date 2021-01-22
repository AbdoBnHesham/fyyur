import os

SECRET_KEY = os.getenv('SECRET_KEY')
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True #Enabling it in .env

# Connect to the database
# DONE IMPLEMENT DATABASE URL
if not os.getenv('DATABASE_URI'):
    print(' $ IMPORTANT INFO: using SQLITE in memory because there is no value for DATABASE_URI.')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or 'sqlite:///:memory:'  # defaults to sqlite in memory

# To suppress FSADeprecationWarning warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
