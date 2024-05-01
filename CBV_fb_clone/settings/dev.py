from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'CBV_FOR_PYTEST',      
        'USER': 'postgres',
        'PASSWORD': '12345', 
        # 'HOST': 'db',
        'HOST': 'localhost',
        'PORT': '5432', 
    }
}