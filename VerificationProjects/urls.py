"""
URL configuration for VerificationProjects project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from django.conf import settings
from VerificationProjects.settings import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/verification/', include('applications.verification.urls')),
    path('api/v1/users/', include('applications.users.urls')),
    path('api/v1/bosspage/', include('applications.boss.urls')),
    path('api/v1/establishment/', include('applications.establishment.urls')),
    path('api/v1/employee/', include('applications.employee.urls')),
    path('set_language/', set_language, name='set_language'),
]
urlpatterns += swagger.urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
