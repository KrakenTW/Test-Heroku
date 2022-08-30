from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from services.forms import ServiceForm
from services.models import Service


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    paginate_by = 10
    ordering = "-pk"


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    extra_context = {"header": "Dodawanie usługi"}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['provider'] = self.kwargs.get("provider_pk", "")
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("provider_detail", kwargs={"pk": self.object.provider.pk})


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy("owner_service_list")

    # TODO: Create confirmation in js
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    extra_context = {"header": "Edycja usługi"}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("provider_detail", kwargs={"pk": self.object.provider.pk})


class OwnersServiceListView(LoginRequiredMixin, ListView):
    """ List view of Services that belongs to user """
    model = Service
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)
