from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Django Admin
    path('admin/', admin.site.urls),
    # Main page 
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    # apps url
    path("users/", include("users.urls")),
    path("product/", include("product.urls")),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
