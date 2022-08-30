from django.urls import path

from services.views import (
    ServiceCreateView,
    ServiceDeleteView,
    ServiceDetailView,
    ServiceListView,
    ServiceUpdateView,
    OwnersServiceListView,
)

urlpatterns = [
    path("", ServiceListView.as_view(), name="service_list"),
    path("add", ServiceCreateView.as_view(), name="add_service"),
    path("add/<int:provider_pk>", ServiceCreateView.as_view(), name="add_service"),
    path("edit/<int:pk>/", ServiceUpdateView.as_view(), name="edit_service"),
    path("delete/<int:pk>/", ServiceDeleteView.as_view(), name="delete_service"),
    path("<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    # Owner urls
    path("cms", OwnersServiceListView.as_view(), name="owner_service_list"),
]
