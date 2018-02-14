from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Organization
from ..views import OrganizationsViews


class OrganizationViewTests(TestCase):
    def setUp(self):
        self.orgaization = Organization.objects.create(
            name="Githubtraining",
            slug="githubtraining",
            description="Some Desc",
            github_org_key_name="description",
        )
        home_url = reverse('home')
        organizations_urls = reverse('organization:organizations')

        self.response_home_url = self.client.get(home_url)
        self.response_organizations_url = self.client.get(organizations_urls)

    def test_home_view_status_code(self):
        self.assertEquals(self.response_home_url.status_code, 200)

    def test_organization_view_status_code(self):
        self.assertEquals(self.response_organizations_url.status_code, 200)

    def test_home_url_resolves_organizations_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, OrganizationsViews)

    def test_organizations_url_resolves_organizations_view(self):
        view = resolve('/organization/')
        self.assertEquals(view.func.view_class, OrganizationsViews)

    def test_organizations_all_url_resolves_organizations_view(self):
        view = resolve('/organization/all/')
        self.assertEquals(view.func.view_class, OrganizationsViews)
