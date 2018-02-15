from django.test import TestCase
from django.urls import resolve, reverse
from django.conf import settings

from ..models import Organization, Repository


class GetRepositoriesJsonMethodTest(TestCase):

    def setUp(self):
        self.new_url = reverse("organization:new_organization")

        data_organization_1 = {
            'name': "Githubtraining",
            'description': "Some Desc",
            'github_org_key_name': "githubtraining",
        }

        self.client.post(self.new_url, data_organization_1)

        data_organization_2 = {
            'name': "Continuum",
            'description': "Continuum",
            'github_org_key_name': "continuum",
        }

        self.client.post(self.new_url, data_organization_2)

    def test_returns_only_list_of_dicts(self):
        org = Organization.objects.all()[0]
        self.assertIsInstance(org.get_repositories_json()[0], dict)

    def test_returns_only_list_of_repository_objects(self):
        org = Organization.objects.all()[0]
        self.assertIsInstance(org.get_repositories_json(as_repository_objects=True)[0], Repository)

    def test_returns_filter_by_name(self):
        org = Organization.objects.get(slug="continuum")
        self.assertEquals(len(org.get_repositories_json(filter_by_name="espinita")), 1)

        org = Organization.objects.get(slug="githubtraining")
        self.assertEquals(len(org.get_repositories_json(as_repository_objects=True, filter_by_name="example")), 17)

    def test_returns_filter_by_name_and_order_by_github_created_at_desc(self):
        org = Organization.objects.get(slug="githubtraining")
        repo = org.get_repositories_json(as_repository_objects=True, filter_by_name="example", order_by="-github_created_at")[0]
        self.assertEquals(repo.github_id, 33316062)

    def test_returns_filter_by_name_and_order_by_github_updated_at_desc(self):
        org = Organization.objects.get(slug="githubtraining")
        repo = org.get_repositories_json(as_repository_objects=True, filter_by_name="example", order_by="-github_updated_at")[0]
        self.assertEquals(repo.github_id, 11904120)

    def test_returns_order_by_github_created_at_asc(self):
        org = Organization.objects.get(slug="githubtraining")
        repo = org.get_repositories_json(as_repository_objects=True, order_by="github_created_at")[0]
        self.assertEquals(repo.github_id, 9104334)

    def test_returns_order_by_github_updated_at_asc(self):
        org = Organization.objects.get(slug="githubtraining")
        repo = org.get_repositories_json(as_repository_objects=True, order_by="github_updated_at")[0]
        self.assertEquals(repo.github_id, 11904134)
