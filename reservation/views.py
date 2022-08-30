from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from reservation.forms import ReservationServiceForm
from reservation.models import Reservation, ReservationService
from services.models import Service


class UsersReservationListView(ListView):
    model = Reservation
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


class UserReservationDetailView(DetailView):
    model = Reservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservation_services'] = self.object.reservation_services.all()
        return context


class UserReservationReserve(View):
    def post(self, request, *args, **kwargs):
        reservation_pk = kwargs.pop('pk')
        self.object = Reservation.objects.get(pk=reservation_pk)
        reservation = self.object
        reservation.active = True
        reservation.calculate_total_price()
        reservation.save()
        return HttpResponseRedirect(reverse_lazy('reservation_list'))


class UserReservationServiceCreateView(CreateView):
    model = ReservationService
    form_class = ReservationServiceForm
    template_name = 'reservation/reservation_create.html'
    success_url = reverse_lazy('reservation_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['service'] = self.get_service()
        initial['reservation'] = self.get_reservation()
        initial['price'] = self.get_price()
        return initial

    def get_service(self):
        service_pk = self.kwargs.get("pk", "")
        return service_pk

    def get_reservation(self):
        reservation, created = Reservation.objects.get_or_create(user=self.request.user, active=False,
                                                                 defaults={'total_price': 0})
        return reservation

    def get_price(self):
        service = Service.objects.get(pk=self.get_service())
        return service.price
