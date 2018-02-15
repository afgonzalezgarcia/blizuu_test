# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from utils.utils import slug_generator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from .models import Organization, Repository
from .forms import *

# Create your views here.

class OrganizationsViews(ListView):
    model = Organization
    context_object_name = 'organizations'
    template_name = "organizations.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        action = self.request.GET.get("action",  False)
        if action:
            organization_slug = self.request.GET.get("organization",  False)
            if Organization.objects.filter(slug=organization_slug).exists():
                organization = Organization.objects.get(slug=organization_slug)
                kwargs['alert_message'] = "%s has been %s" % (organization, action)
                kwargs['alert_message_success'] = True

        kwargs['items'] = super(OrganizationsViews, self).get_context_data().get(self.context_object_name)
        kwargs['tcontext_objects_name'] = "Organizations"
        return super(OrganizationsViews, self).get_context_data(**kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-id')
        return queryset


class OrganizationCreateView(CreateView):
    model = Organization
    context_object_name = 'organization'
    form_class = OrganizationForm
    template_name = "new_organization.html"

    def get_context_data(self, **kwargs):
        kwargs['model'] = self.model
        kwargs['tcontext_objects_name'] = "Organizations"
        return super(OrganizationCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.slug = slug_generator(organization.name, self.model)
        organization.save()
        self.synchronization_response = organization.synchronize_repositories()
        redirect_to = "%s%s" % (reverse('organization:organizations'), "?action=created&organization=%s" % (organization.slug))
        return redirect(redirect_to)

class OrganizationUpdateView(UpdateView):
    model = Organization
    context_object_name = 'organization'
    form_class = OrganizationForm
    template_name = "new_organization.html"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        kwargs['model'] = self.model
        kwargs['tcontext_objects_name'] = "Organizations"
        return super(OrganizationUpdateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.save()
        self.synchronization_response = organization.synchronize_repositories()
        redirect_to = "%s%s" % (reverse('organization:organizations'), "?action=updated&organization=%s" % (organization.slug))
        return redirect(redirect_to)


class RepositoriesViews(ListView):
    model = Repository
    context_object_name = 'repositories'
    template_name = "repositories.html"
    redirect_to = None
    search_params = None
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['tcontext_objects_name'] = "Repositories"
        kwargs['organization'] = self.organization
        kwargs['repositories_search_form'] = self.repositories_search_form

        if self.search_params is not None:
            kwargs['search_params'] = self.search_params

        action = self.request.GET.get("action",  False)
        if action:
            if action == "syncronized":
                success = self.request.GET.get("success",  False)
                message = self.request.GET.get("message",  False)
                if action and message:
                    kwargs['alert_message'] = urllib.unquote_plus(message)
                    if success == "True":
                        kwargs['alert_message_success'] = True
                    else:
                        kwargs['alert_message_success'] = False

        kwargs['items'] = super(RepositoriesViews, self).get_context_data().get(self.context_object_name)
        return super(RepositoriesViews, self).get_context_data(**kwargs)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        order_by = "created_at"
        filters = {}

        if self.repositories_search_form.is_bound:
            if self.repositories_search_form.data.get("order_by", False):
                order_by = self.repositories_search_form.data.get("order_by")

            name = self.repositories_search_form.data.get("name", False)
            if name:
                filters.update({'name__contains': name})

        queryset = self.get_queryset().filter(**filters).order_by("github_%s" % order_by)
        repositories_json_objects = self.organization.get_repositories_json(as_repository_objects=True, order_by=order_by, filter_by_name=name)
        paginator_queryset = [repository for repository in queryset] + [repository for repository in repositories_json_objects]
        return super(RepositoriesViews, self).get_paginator(paginator_queryset, self.paginate_by, **kwargs)

    def get_queryset(self):
        self.organization = get_object_or_404(Organization, pk=self.kwargs.get('pk'))
        queryset = self.organization.repositories.all()
        return queryset

    def get(self, request, *args, **kwargs):
        self.organization = get_object_or_404(Organization, pk=self.kwargs.get('pk'))
        self.repositories_search_form = RepositoriesSearchForm(self.request.GET)
        action = self.kwargs.get("action", None)

        if action is not None and action == "synchronize-repositories":
            synchronization_response = self.organization.synchronize_repositories()
            success = False
            message = ""
            if synchronization_response:
                message = synchronization_response.get("message")
                if synchronization_response["success"]:
                    success = True
            self.redirect_to = "%s%s" % (reverse('organization:repositories', kwargs={'pk': self.organization.id, 'action': 'repositories'}), "?action=syncronized&success=%s&message=%s" % (success, urllib.quote_plus(message)))
            return redirect(self.redirect_to)
        elif action == "repositories":
            if "name" in self.request.GET and "order_by" in self.request.GET:
                params = self.request.get_full_path().split("?")[1]
                params = params.split("&")
                params = [param for param in params if not param.startswith("page=")]
                self.search_params = "&".join(params)
        else:
            raise Http404("Page not found")

        return super(RepositoriesViews, self).get(request, *args, **kwargs)
