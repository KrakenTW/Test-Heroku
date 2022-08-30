from django.urls import path

from providers.views import (
    ProviderDetailView,
    ProviderListView,
    ProviderDeleteView,
    OwnersProviderListView, ProviderCreateView,
)

urlpatterns = [
    path("", ProviderListView.as_view(), name="provider_list"),
    path("delete/<int:pk>/", ProviderDeleteView.as_view(), name="delete_provider"),
    path("<int:pk>/", ProviderDetailView.as_view(), name="provider_detail"),
    # Owner urls
    path("cms", OwnersProviderListView.as_view(), name="owners_provider_list"),
    path("add", ProviderCreateView.as_view(), name="add_provider"),

]
