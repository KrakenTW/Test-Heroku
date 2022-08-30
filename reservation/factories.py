import random

import factory.fuzzy
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from reservation.models import Reservation
from services.factories import ServiceFactory


class ReservationFactory(DjangoModelFactory):
    total_price = 10.2
    user = factory.SubFactory(UserFactory)
    active = True

    class Meta:
        model = Reservation


class ReservationServiceFactory(DjangoModelFactory):
    service = factory.SubFactory(ServiceFactory)
    price = factory.LazyAttribute(random.randrange(1, 100 + 1))
    reservation = factory.SubFactory(ReservationFactory)
