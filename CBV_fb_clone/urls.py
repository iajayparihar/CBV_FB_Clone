from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from CBV_fb_clone.apps import *
# import django.contrib.auth.urls
from CBV_fb_clone.apps import api_urls

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# def trigger_error(request):
#     division_by_zero = 1 / 0

    # path('sentry-debug/', trigger_error),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/',include('post.urls')), 
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/',include('register.urls')),
    
    path('api/',include('api_urls.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

