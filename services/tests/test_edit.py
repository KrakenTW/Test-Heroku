from decimal import Decimal

from django.test import TestCase

from accounts.factories import UserFactory
from providers.factories import ProviderFactory
from services.factories import ServiceFactory
from services.models import Service
from utils.tests.mixins import TestUtilityMixin


class TestEdit(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.service = ServiceFactory.create(created_by=self.user)
        self.url = f"/services/edit/{self.service.id}/"

    def test_user_cant_enter_edit_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_see_edit_form_after_log_in(self):
        self.__given_user_logged_in()
        response = self.client.get(self.url)
        self.assertContains(response, "Edycja usługi")

    def test_user_redirected_after_success_edit(self):
        self.__given_user_logged_in()
        provider = ProviderFactory.create(user=self.user)
        response = self.client.post(
            self.url,
            {
                "title": "new title",
                "description": "opis",
                "price": Decimal("99.21"),
                "provider": provider.pk,
            },
        )
        self.__then_service_title_and_price_changed()
        self.__then_redirected_to_service_list(response)

    def test_user_get_404_when_edit_non_existing_service(self):
        self.__given_user_logged_in()
        non_existing_service_id = self.service.id + 1
        url = f"services/edit/{non_existing_service_id}"
        response = self.client.post(
            url,
            {"title": "new title", "description": "opis", "price": Decimal("99.21")},
        )
        self.assertEqual(response.status_code, self.STATUS_NOT_FOUND)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __then_service_title_and_price_changed(self):
        service = Service.objects.get(pk=self.service.id)
        self.assertEqual(service.title, "new title")
        self.assertEqual(service.price, Decimal("99.21"))

    def __then_redirected_to_service_list(self, response):
        self.was_redirected_to("/services/", response)
