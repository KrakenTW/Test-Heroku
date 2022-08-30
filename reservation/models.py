from django.db import models
from django.db.models import Sum

from services.models import Service
from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=7)
    active = models.BooleanField(default=False)

    def calculate_total_price(self):
        self.total_price = ReservationService.objects.filter(reservation=self).aggregate(total_price=Sum('price'))[
            'total_price']
        return self.total_price

    def __str__(self):
        return f"id: {self.pk} price: {self.total_price} active {self.active}"


class ReservationService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reservation_services')

    def __str__(self):
        return f"{self.service} date: {self.date} cost: {self.price}"
