import factory.fuzzy
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from providers.models import Provider


class ProviderFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "title_%d" % n)
    description = factory.Sequence(lambda n: "description_%d" % n)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Provider
