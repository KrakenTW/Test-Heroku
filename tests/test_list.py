from django.test import TestCase

from providers.factories import ProviderFactory
from utils.tests.mixins import TestUtilityMixin


class TestList(TestCase, TestUtilityMixin):
    url = "/"

    def setUp(self):
        self.providers_per_page = 10
        self.paging_element = "paging_grip"

    def test_returns_single_provider(self):
        provider = ProviderFactory.create()
        response = self.client.get(self.url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertContains(response, provider.name)

    def test_returns_ok_when_there_are_multiple_page_of_services(
        self,
    ):
        ProviderFactory.create_batch(size=self.providers_per_page + 1)

        response = self.client.get(self.url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertContains(response, "&laquo;")
