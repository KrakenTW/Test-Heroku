from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.views.generic.edit import FormMixin
from providers.forms import ProviderFilterForm, ProviderForm
from providers.models import Provider


class ProviderListView(FormMixin, ListView):
    model = Provider
    paginate_by = 10
    form_class = ProviderFilterForm

    def get_queryset(self):
        queryset = self.model.objects.search(**self.request.GET.dict())
        return queryset


class ProviderDetailView(DetailView):
    model = Provider

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = self.object.services.all()
        return context


class ProviderDeleteView(LoginRequiredMixin, DeleteView):
    model = Provider
    success_url = reverse_lazy("owners_provider_list")

    # TODO: Create confirmation in js
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class OwnersProviderListView(LoginRequiredMixin, ProviderListView):
    """ List view of Providers that belongs to user """

    def get_queryset(self):
        filters = self.request.GET.dict()
        filters["user"] = self.request.user
        return self.model.objects.search(**filters)


class ProviderCreateView(LoginRequiredMixin, CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'providers/provider_create.html'

    success_url = None
    extra_context = {"header": "Dodawanie firmy"}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.user = request.user
        inlines = form.services_formset(request.POST, instance=form.instance)
        for inline in inlines:
            inline.instance.created_by = request.user

        if form.is_valid() and inlines.is_valid():
            self.object = form.save()
            inlines.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('provider_detail', kwargs={'pk': self.object.pk})
