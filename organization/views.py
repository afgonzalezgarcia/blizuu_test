# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.views.generic import CreateView, ListView, RedirectView, TemplateView, UpdateView
from django.utils.text import slugify

from .models import Organization, Repository
from .forms import *

# Create your views here.

class OrganizationsViews(ListView):
    model = Organization
    context_object_name = 'organizations'
    template_name = "organizations.html"

    def get_context_data(self, **kwargs):
        kwargs['todos'] = self.get_queryset()
        kwargs['tcontext_objects_name'] = "Organizations"
        return super(OrganizationsViews, self).get_context_data(**kwargs)


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
        organization.slug = slugify(organization.name)
        organization.save()
        self.synchronization_response = organization.synchronize_repositories()

        return redirect('organization:organizations')

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
        return redirect('organization:organizations')


class RepositoriesViews(ListView):
    model = Repository
    context_object_name = 'repositories'
    template_name = "repositories.html"
    synchronization_response = None
    todos = model.objects.none()

    def get_context_data(self, **kwargs):
        kwargs['tcontext_objects_name'] = "Repositories"
        kwargs['organization'] = self.organization
        kwargs['todos'] = self.todos

        if self.synchronization_response:
            kwargs["synchronization_message"] = self.synchronization_response.get("message")
            if self.synchronization_response["success"]:
                kwargs["synchronized"] = True
            else:
                kwargs["synchronized"] = False

        return super(RepositoriesViews, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.organization = get_object_or_404(Organization, pk=self.kwargs.get('pk'))
        action = self.kwargs.get("action", None)

        if action is not None and action == "synchronize-repositories":
            self.synchronization_response = self.organization.synchronize_repositories()
        elif action == "repositories":
            pass
        else:
            raise Http404("Page not found")

        queryset = self.organization.repositories.order_by('-github_created_at')
        self.todos = queryset
        return queryset
