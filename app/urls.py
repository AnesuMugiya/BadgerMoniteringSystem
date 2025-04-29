"""
URL configuration for app project.

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

# Handles static files media and images
from django.conf import settings
from django.conf.urls.static import static

# Urls from Users application
from users import views as user_views
# Urls from Django's autehnticating applications
from django.contrib.auth import views as auth_views

urlpatterns = [
    # The URL pattern for the admin interface
    # This allows you to access the admin interface at /admin/
    path('admin/', admin.site.urls),
    
    # The URL pattern for the users application
    path('register/', user_views.register, name='register'),
    path('account/', user_views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('core.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)