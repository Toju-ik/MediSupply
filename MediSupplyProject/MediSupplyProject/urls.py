"""
URL configuration for MediSupplyProject project.

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
from django.views.generic import RedirectView

urlpatterns = [
    # 1. Admin site
    path('admin/', admin.site.urls),

    # 2. Authentication (login/logout) URLs
    path('accounts/', include('django.contrib.auth.urls')),

    # 3. Redirect the root URL to /orders/
    path('', RedirectView.as_view(url='orders/', permanent=False)),

    # 4. All other URLs are handled
    path('', include('mediapp.urls')),



]
