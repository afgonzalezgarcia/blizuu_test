# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import requests

from dateutil.parser import parse
from django.conf import settings
from django.contrib.postgres import fields as postgres_fields
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Organization(models.Model):
    name = models.CharField(_("name"), max_length=150)
    slug = models.SlugField(_("slug"), max_length=150, unique=True)
    description = models.TextField(_("description"), blank=True)
    active = models.BooleanField(_("active"), default=True)
    github_org_key_name = models.CharField(_("organization key name in github"), max_length=150, help_text=_("Your organization key name in github"))
    last_sync_at = models.DateTimeField(_("last synchronization"), blank=True, null=True)
    repositories_json = postgres_fields.JSONField(blank=True, default=[])

    # timestamps
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = "organization"
        verbose_name = _("organization")
        verbose_name = _("organizations")

    def __unicode__(self):
        return self.name

    def synchronize_repositories(self, *args, **kwargs):
        proccess_info = {
            "success": False,
            "data": None,
            "message": "",
            "api_response": None,
        }

        if self.github_org_key_name:
            api_repos_url = "%s/orgs/%s/repos" % (settings.GITHUB_API_BASE_URL, self.github_org_key_name)

            if (hasattr(settings, 'GITHUB_CLIENT_ID') and settings.GITHUB_CLIENT_ID) and (hasattr(settings, 'GITHUB_CLIENT_SECRET') and settings.GITHUB_CLIENT_SECRET):
                api_repos_url = "%s?client_id=%s&client_secret=%s" % (api_repos_url, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)

            response = requests.get(api_repos_url)
            if response.status_code == requests.codes.ok:
                repositories = []
                if response.json():
                    repositories = response.json()
                    self.last_sync_at = timezone.now()
                    self.repositories_json = repositories
                    self.save()
                    reversed_repositories = sorted(repositories, key=lambda repos: repos["id"], reverse=True)

                    if self.repositories.count():
                        if hasattr(settings, "MAX_REPOSITORIES_IN_BD"):
                            for repository in reversed_repositories[:settings.MAX_REPOSITORIES_IN_BD]:
                                Repository.update_or_create_from_json(repository, self)

                            if self.repositories.count() > settings.MAX_REPOSITORIES_IN_BD:
                                ids_to_delete = self.repositories.all().order_by("-github_id").values_list("id", flat=True)[settings.MAX_REPOSITORIES_IN_BD:]
                                Repository.objects.filter(id__in=ids_to_delete).delete()
                        else:
                            for repository in reversed_repositories[:settings.MAX_REPOSITORIES_IN_BD]:
                                Repository.update_or_create_from_json(repository, self)

                    else:
                        for repository in reversed_repositories[:10]:
                            Repository.update_or_create_from_json(repository, self)

                proccess_info["message"] = "Repositories to %s has been synchronized" % (self)
                proccess_info["success"] = True
                proccess_info["data"] = repositories
            else:
                proccess_info["message"] = response.json().get("message")
        else:
            proccess_info["message"] = "The value 'github_org_key_name' is empty or invalid, please check ir"

        return proccess_info

    def get_repositories_json(self, *args, **kwargs):
        """
        Returns all repositories except stored repos
        """
        stored_ids = self.repositories.all().values_list("github_id", flat=True)
        as_repository_objects = kwargs.get("as_repository_objects", False)
        filter_by_name = kwargs.get("filter_by_name", False)
        order_by = kwargs.get("order_by", False)

        if order_by:
            if order_by.startswith("-"):
                order_by_reverse = "True"
                order_by = order_by.replace("-", "")
            else:
                order_by_reverse = "False"

        if as_repository_objects:
            item_creation_sentence = "Repository.get_repository_object_from_json(repository, self)"
            order_by_sentence = "repo: repo.%s" % (order_by)
        else:
            item_creation_sentence = "repository"

            # because originaries fields from github called created_at non github_created_at
            if order_by and order_by.startswith("github_"):
                order_by = order_by.replace("github_", "")

            order_by_sentence = "repo: repo['%s']" % (order_by)

        if filter_by_name:
            repositories = eval("[%s for repository in self.repositories_json if repository['id'] not in stored_ids and (filter_by_name in repository['name'])]" % item_creation_sentence)
        else:
            repositories = eval("[%s for repository in self.repositories_json if repository['id'] not in stored_ids]" % item_creation_sentence)

        if order_by:
            repositories = eval("sorted(repositories, key=lambda %s, reverse=%s)" % (order_by_sentence, order_by_reverse))

        return repositories


class Repository(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="repositories")

    github_id = models.IntegerField(_("github id"), blank=True, default=0)
    name = models.CharField(_("name"), max_length=200)
    full_name = models.CharField(_("full name"), max_length=200, blank=True, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    active = models.BooleanField(default=True)

    api_url = models.URLField(_("api url"))
    html_url = models.URLField(_("api url"), blank=True, null=True)

    github_created_at = models.DateTimeField(_("creation date in github"), blank=True, null=True)
    github_updated_at = models.DateTimeField(_("updated date in github"), blank=True, null=True)
    github_pushed_at = models.DateTimeField(_("pushed date in github"), blank=True, null=True)

    github_data = postgres_fields.JSONField(blank=True, default=[])

    # timestamps
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("repository")
        verbose_name = _("repositories")

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_values_from_json(json, organization):
        values = {
            'organization': organization,
            'name': json.get("name", "Name"),
            'github_id': json.get("id"),
            'full_name': json.get("full_name"),
            'description': json.get("description", "Some Description"),
            'api_url': json.get("url"),
            'html_url': json.get("html_url"),
            'github_created_at': None,
            'github_updated_at': None,
            'github_pushed_at': None,
            'github_data': json,
        }

        if json.get("created_at"):
            values["github_created_at"] = parse(json.get("created_at"))

        if json.get("updated_at"):
            values["github_updated_at"] = parse(json.get("updated_at"))

        if json.get("pushed_at"):
            values["github_pushed_at"] = parse(json.get("pushed_at"))

        return values

    @staticmethod
    def update_or_create_from_json(json, organization):
        values = Repository.get_values_from_json(json, organization)
        obj, created = Repository.objects.update_or_create(
            github_id=json.get("id"), organization=organization,
            defaults=values,
        )

        return obj, created

    @staticmethod
    def get_repository_object_from_json(json, organization):
        values = Repository.get_values_from_json(json, organization)
        return Repository(**values)
