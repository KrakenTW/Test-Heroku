from django.test import TestCase

from accounts.factories import UserFactory
from services.factories import ServiceFactory
from services.models import Service
from utils.tests.mixins import TestUtilityMixin


class TestDelete(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.service = ServiceFactory.create(created_by=self.user)
        self.url = f"/services/delete/{self.service.id}/"

    def test_user_cant_delete_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_delete_after_log_in(self):
        self.__given_user_logged_in()
        before = Service.objects.count()
        response = self.client.post(self.url)
        after = Service.objects.count()
        self.assertEqual(before, after + 1)
        self.__then_redirected_to_service_list(response)

    def test_user_get_404_when_delete_non_existing_service(self):
        self.__given_user_logged_in()
        non_existing_service_id = self.service.id + 1
        url = f"services/delete/{non_existing_service_id}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.STATUS_NOT_FOUND)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __then_redirected_to_service_list(self, response):
        self.was_redirected_to("/services/", response)
