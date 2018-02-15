from django.test import TestCase
from django.urls import resolve, reverse
from django.conf import settings

from ..models import Organization, Repository
from ..views import RepositoriesViews, RepositoriesSearchForm

class RepositoriesViewTest(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            name="Githubtraining",
            slug="githubtraining",
            description="Some Desc",
            github_org_key_name="githubtraining",
        )

        self.repositories_url = reverse("organization:repositories", kwargs={'pk': self.organization.id, 'action': 'repositories'})
        self.synchronize_url = reverse("organization:repositories", kwargs={'pk': self.organization.id, 'action': 'synchronize-repositories'})
        self.response_repositories_url = self.client.get(self.repositories_url)

    def test_repositories_view_repositories_action_status_code(self):
        self.assertEquals(self.response_repositories_url.status_code, 200)

    def test_repositories_url_action_repositories_resolve_repositories_view(self):
        view = resolve(self.repositories_url)
        self.assertEquals(view.func.view_class, RepositoriesViews)

    def test_contains_form(self):
        form = self.response_repositories_url.context.get('repositories_search_form')
        self.assertIsInstance(form, RepositoriesSearchForm)

    def test_items_is_empty_in_repositories_view_context(self):
        items = self.response_repositories_url.context.get('items')
        # self.assertIsInstance(items, QuerySet)
        self.assertEquals(len(items), 0)

    def test_repositories_view_synchronize_repositories_action_status_code(self):
        self.response_synchronize_url = self.client.get(self.synchronize_url)
        self.assertEquals(self.response_synchronize_url.status_code, 302)

    def test_repositories_url_action_synchronize_repositories_repositories_view(self):
        view = resolve(self.synchronize_url)
        self.assertEquals(view.func.view_class, RepositoriesViews)

    def test_repositories_views_synchronize_successfully(self):
        self.assertEquals(self.organization.repositories.count(), 0)
        self.response_synchronize_url = self.client.get(self.synchronize_url)
        self.assertEquals(self.organization.repositories.count(), 10)

    def test_repositories_views_raise_404_to_invalid_organization(self):
        invalid_url = reverse("organization:repositories", kwargs={'pk': 10000, 'action': 'repositories'})
        invalid_response = self.client.get(invalid_url)
        self.assertEquals(invalid_response.status_code, 404)

    def test_repositories_views_raise_404_to_invalid_action(self):
        invalid_url = reverse("organization:repositories", kwargs={'pk': 10000, 'action': 'invalid-action'})
        invalid_response = self.client.get(invalid_url)
        self.assertEquals(invalid_response.status_code, 404)
