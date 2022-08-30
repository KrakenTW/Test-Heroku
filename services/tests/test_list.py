from django.test import TestCase

from accounts.factories import UserFactory
from services.factories import ServiceFactory
from utils.tests.mixins import TestUtilityMixin


class TestList(TestCase, TestUtilityMixin):
    url = "/services/"

    def setUp(self):
        self.user = UserFactory.create()
        self.service_per_page = 10
        self.paging_element = "paging_grip"

    def test_user_cant_see_service_list_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    # def test_user_can_see_his_services_after_log_in(self):
    #     self.__given_user_logged_in()
    #     self.__given_services_created(title="test service")
    #     response = self.client.get(self.url)
    #     self.__then_logged_in_user_services_shown(response)

    def test_returns_ok_when_there_are_multiple_page_of_services(
        self,
    ):
        self.__given_user_logged_in()
        ServiceFactory.create_batch(
            size=self.service_per_page + 1, created_by=self.user
        )

        response = self.client.get(self.url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertContains(response, "&laquo;")

    # def test_returns_matched_item(self):
    #     self.__given_user_logged_in()
    #     self.__given_services_created(title="item")
    #     url = f"{self.url}?title__icontains=item"
    #     response = self.client.get(url)
    #     self.assertEqual(self.STATUS_OK, response.status_code)
    #     self.assertContains(response, "item")

    # def test_returns_no_items_if_no_one_match(self):
    #     self.__given_user_logged_in()
    #     self.__given_services_created(title="test")
    #     url = f"{self.url}?title__icontains=noexisting"
    #     response = self.client.get(url)
    #     self.assertEqual(self.STATUS_OK, response.status_code)
    #     self.assertNotContains(response, "test")

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __given_services_created(self, **kwargs):
        ServiceFactory.create(**kwargs, created_by=self.user)
