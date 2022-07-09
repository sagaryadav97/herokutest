from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from Books import views
schema_view = get_schema_view(
   openapi.Info(
      title="LMS API",
      default_version='v1',
      description="Library Management System App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
) 
urlpatterns = [
   path('', views.index),
   path('admin/', admin.site.urls),
   path('user/',include('Users.urls')),
   path('book/',include('Books.urls')),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #http://localhost:8000/swagger/ 
]