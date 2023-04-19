from .base import *

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(",")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG']

CORS_ALLOWED_ORIGINS = [os.environ['CORS_ALLOWED_ORIGINS']]

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = json.loads(os.environ['CLOUDINARY_STORAGE'])

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'