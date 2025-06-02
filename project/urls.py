"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from task.routers.routers import router as task_router
from user.routers.routers import router as user_router

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.registry.extend(task_router.registry)
router.registry.extend(user_router.registry)

schema_view = get_schema_view(
   openapi.Info(
      title="Task API",
      default_version='v1',
      description="Task Management System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kripahayanju@gmail.com"),
      license=openapi.License(name="No License"),
      **{'x-logo': {'url': '  '}},
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
from task.viewsets.task_viewsets import taskViewsets
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', obtain_auth_token),
    # API Authentication
    path('v1/api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]