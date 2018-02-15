from django.test import TestCase
from django.urls import resolve, reverse
from django.conf import settings

from ..forms import OrganizationForm
from ..models import Organization, Repository
from ..views import OrganizationCreateView, OrganizationUpdateView

class OrganizationCreateViewTest(TestCase):

    def setUp(self):
        self.new_url = reverse("organization:new_organization")
        self.response_new_url = self.client.get(self.new_url)

    def test_organization_create_view_status_code(self):
        self.assertEquals(self.response_new_url.status_code, 200)

    def test_new_url_resolves_organization_create_view(self):
        view = resolve("/organizations/new/")
        self.assertEquals(view.func.view_class, OrganizationCreateView)

    def test_csrf(self):
        self.assertContains(self.response_new_url, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response_new_url.context.get('form')
        self.assertIsInstance(form, OrganizationForm)

    def test_new_organization_valid_post_data(self):
        data = {
            'name': "Githubtraining",
            'description': "Some Desc",
            'github_org_key_name': "githubtraining",
        }

        self.client.post(self.new_url, data)
        self.assertTrue(Organization.objects.exists())
        self.assertEquals(Organization.objects.count(), 1)
        self.assertEquals(Organization.objects.filter(slug="githubtraining").count(), 1)
        self.assertTrue(Repository.objects.filter(organization__slug="githubtraining").exists())
        self.assertEquals(Repository.objects.filter(organization__slug="githubtraining").count(), settings.MAX_REPOSITORIES_IN_BD)

    def test_new_organization_valid_post_data_invalid_github_org_key_name(self):
        data = {
            'name': "Continuum",
            'description': "Continuum",
            'github_org_key_name': "Continuum123",
        }

        self.client.post(self.new_url, data)
        self.assertTrue(Organization.objects.exists())
        self.assertEquals(Organization.objects.count(), 1)
        self.assertEquals(Organization.objects.filter(slug="continuum").count(), 1)
        self.assertFalse(Repository.objects.filter(organization__slug="continuum").exists(), False)
        self.assertEquals(Repository.objects.filter(organization__slug="continuum").count(), 0)

    def test_new_organization_same_name_create_different_slug(self):
        organization1 = {
            'name': "Organization",
            'description': "Continuum",
            'github_org_key_name': "organization1",
        }

        organization2 = {
            'name': "Organization",
            'description': "Continuum",
            'github_org_key_name': "organization2",
        }

        self.client.post(self.new_url, organization1)
        self.assertTrue(Organization.objects.filter(slug="organization").exists())
        self.assertEquals(Organization.objects.filter(slug="organization").count(), 1)

        self.client.post(self.new_url, organization2)
        self.assertTrue(Organization.objects.filter(slug="organization-1").exists())
        self.assertEquals(Organization.objects.filter(slug="organization-1").exists(), 1)

    def test_new_organization_invalid_post_data(self):
        post_response = self.client.post(self.new_url, {})
        form = post_response.context.get('form')
        self.assertEquals(post_response.status_code, 200)
        self.assertTrue(form.errors)


class OrganizationUpdateViewTest(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Githubtraining",
            slug="githubtraining",
            description="Some Desc",
            github_org_key_name="somedesc1234123412341",
        )

        self.update_url = reverse("organization:update_organization", kwargs={'pk': self.organization.id})
        self.response_update_url = self.client.get(self.update_url)

    def test_organization_update_view_status_code(self):
        self.assertEquals(self.response_update_url.status_code, 200)

    def test_update_url_resolves_organization_update_view(self):
        view = resolve("/organizations/1/update/")
        self.assertEquals(view.func.view_class, OrganizationUpdateView)

    def test_csrf(self):
        self.assertContains(self.response_update_url, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response_update_url.context.get('form')
        self.assertIsInstance(form, OrganizationForm)

    def test_update_organization_valid_post_data(self):
        data = {
            'name': "Githubtraining",
            'description': "Some Desc Updated",
            'github_org_key_name': "somedesc1234123412341",
        }

        self.client.post(self.update_url, data)
        self.assertTrue(Organization.objects.exists())
        self.assertEquals(Organization.objects.count(), 1)
        self.assertEquals(Organization.objects.filter(slug="githubtraining").count(), 1)
        self.assertEquals(Organization.objects.filter(slug="githubtraining", description="Some Desc Updated").count(), 1)
        self.assertFalse(Repository.objects.filter(organization__slug="githubtraining").exists())

    def test_new_organization_valid_post_data_update_github_org_key_name_sync_repos(self):
        data = {
            'name': "Githubtraining",
            'description': "Some Desc Updated",
            'github_org_key_name': "githubtraining",
        }

        self.client.post(self.update_url, data)
        self.assertTrue(Repository.objects.filter(organization__slug="githubtraining").exists())
        self.assertEquals(Repository.objects.filter(organization__slug="githubtraining").count(), settings.MAX_REPOSITORIES_IN_BD)

    def test_update_organization_invalid_post_data(self):
        post_response = self.client.post(self.update_url, {})
        form = post_response.context.get('form')
        self.assertEquals(post_response.status_code, 200)
        self.assertTrue(form.errors)
