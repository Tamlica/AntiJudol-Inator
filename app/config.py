import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'c29jaWFidXp6LWZpbHRlcmluZy13b3JkLWJ5LXByb2plY3QtZG8=')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'cHJvamVjdC1kby1zb2NpYWJ1enotZmlsdGVyaW5nLXdvcmQtand0')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:757377@localhost/sociabuzz_filter'
    SQLALCHEMY_TRACK_MODIFICATIONS = False