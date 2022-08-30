from django.urls import path

from reservation.views import UsersReservationListView, UserReservationDetailView, UserReservationServiceCreateView, \
    UserReservationReserve

urlpatterns = [
    path("", UsersReservationListView.as_view(), name="reservation_list"),
    path("<int:pk>/", UserReservationDetailView.as_view(), name="reservation_detail"),
    path("add/<int:pk>", UserReservationServiceCreateView.as_view(), name="add_to_basket"),
    path("update/<int:pk>", UserReservationReserve.as_view(), name="checkout_reservatuin"),
]
