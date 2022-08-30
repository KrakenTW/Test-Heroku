# import datetime
#
# from django.test import TestCase
#
# from accounts.factories import UserFactory
# from reservation.factories import ReservationFactory
# from services.factories import ServiceFactory
#
#
# class TestReservation(TestCase):
#     def setUp(self) -> None:
#         self.user = UserFactory.create()
#         self.existing_reservation = ReservationFactory.create(user=self.user)
#         self.service = ServiceFactory.create()
#
#     def test_user_can_add_service_to_reservation(self):
#         url = f'/reservation/add/{self.service.pk}'
#         self.client.force_login(self.user, backend=None)
#         response = self.client.post(url, {'reservation': self.existing_reservation,
#                                           'service': self.service,
#                                           'date': datetime.datetime.utcnow() + datetime.timedelta(0, 2)
#                                           })
#         import pdb;pdb.set_trace()
#         self.assertEqual(response.status_code, 301)
