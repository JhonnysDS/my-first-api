# config/prod.py

from default import *

SECRET_KEY = '4b2bf8af88af2a15b2e64a2cbcbea1f7060dea780029952a705b0d51b7f7558ef59cbb14e57d4d8194c13cea7478404acd10'

APP_ENV = APP_ENV_PRODUCTION

SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/blog'