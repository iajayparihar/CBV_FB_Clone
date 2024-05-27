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



from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="FB clone api",
        default_version='v1',),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)
# swagger 
# https://episyche.com/blog/how-to-create-django-api-documentation-using-swagger
# http://127.0.0.1:8000/post/docs/?format=openapi


app_name = "Post"

# from django.contrib.auth.urls
urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),

    path('admin/', admin.site.urls),
    path('post/',include('post.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include('register.urls')),
    
    path('api/',include('api_urls.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

