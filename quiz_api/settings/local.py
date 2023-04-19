from .base import *


INSTALLED_APPS += 'debug_toolbar',

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
HOST = 'http://127.0.0.1:8000'
# URL used to access the media
MEDIA_URL = '/media/'
# JWT_SECRET_KEY = env('JWT_SECRET_KEY')

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES' : [
#         'rest_framework.permissions.AllowAny'
#     ],
# }
FRONT_ORIGIN = env('FRONT_ORIGIN')

SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
# SESSION_COOKIE_DOMAIN = 'http://localhost:8080'
# ALLOWED_HOSTS = ['https://localhost:8080','http://localhost:8080']