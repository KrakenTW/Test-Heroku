from decimal import Decimal

from django.test import TestCase

from accounts.factories import UserFactory
from providers.factories import ProviderFactory
from services.factories import ServiceFactory
from services.models import Service
from utils.tests.mixins import TestUtilityMixin


class TestViewserviceAdd(TestCase, TestUtilityMixin):
    url = "/services/add"

    def setUp(self):
        self.user = UserFactory.create()
        self.existing_service = ServiceFactory.create(created_by=self.user)
        provider = ProviderFactory.create(user=self.user)
        self.new_service_data = {
            "title": "New test service",
            "description": "test description",
            "price": Decimal("111.11"),
            "provider": provider.pk
        }

    def test_not_loged_in_user_cant_add(self):
        response = self.client.post(self.url, self.new_service_data)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_get_service_form(self):
        self.client.force_login(self.user, backend=None)

        url = self.url.format(self.existing_service.id)
        response = self.client_send_request_with_params(url, self.new_service_data)
        self.assertEqual(response.status_code, self.STATUS_OK)

    def test_add_service_when_missing_required_data_fails(self):
        self.client.force_login(self.user, backend=None)

        missing_service_data = {
            "title": "Wont work no value",
        }

        response = self.client_send_post_request(self.url, missing_service_data)
        self.assertFalse(response.context["form"].is_valid())

    def test_add_service_ok(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(self.url, self.new_service_data)
        created_service = Service.objects.get(pk=self.existing_service.pk + 1)
        expected_location = f"/{created_service.provider.pk}/"
        self.assertTrue(self.was_redirected_to(expected_location, response))
        self.assertEqual(created_service.title, self.new_service_data["title"])
        self.assertEqual(
            created_service.price,
            self.new_service_data["price"],
        )
