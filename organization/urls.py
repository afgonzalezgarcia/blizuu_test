from django.conf import settings
from django.conf.urls import include, url

from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView


# Routers provide an easy way of automatically determining the URL conf.
from . import views

app_label = "organization"
urlpatterns = [
    url(r'^$', views.OrganizationsViews.as_view(), name='organizations'),
    url(r'^all/$', views.OrganizationsViews.as_view(), name='organizations_all'),
    url(r'^new/$', views.OrganizationCreateView.as_view(), name='new_organization'),
    url(r'^(?P<pk>\d+)/update/$', views.OrganizationUpdateView.as_view(), name='update_organization'),
    url(r'^(?P<pk>\d+)/(?P<action>[-\w]+)/$', views.RepositoriesViews.as_view(), name='repositories'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
