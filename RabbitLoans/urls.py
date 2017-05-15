"""
Definition of urls for RabbitLoans.
"""

import django.contrib.auth.views

from django.conf.urls import url, include
from loans import views
from rest_framework.routers import DefaultRouter

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'loans', views.LoanViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Example:
    #url(r'^$', app.views.home, name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
