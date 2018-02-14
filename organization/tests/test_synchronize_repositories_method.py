from django.test import TestCase
from django.urls import resolve, reverse
from django.conf import settings

from ..models import Organization, Repository

class SynchronizeRepositoriesMethodTest(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Githubtraining",
            slug="githubtraining",
            description="Some Desc",
            github_org_key_name="0",
        )

    def test_dont_synchronize_with_empty_github_org_key_name(self):
        response = self.organization.synchronize_repositories()
        self.assertFalse(response.get("success"))

    def test_dont_synchronize_with_non_existent_github_org_key_name(self):
        self.organization.github_org_key_name = "somecrazygithubname123123123123"
        self.organization.save()

        response = self.organization.synchronize_repositories()
        self.assertFalse(response.get("success"))

    def test_synchronize_success(self):
        self.organization.github_org_key_name = self.organization.slug
        self.organization.save()

        self.assertEquals(self.organization.repositories.count(), 0)
        self.organization.synchronize_repositories()
        self.assertEquals(self.organization.repositories.count(), 10)
