from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class ProviderQuerySet(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get("name", ""):
            qs = qs.filter(name__icontains=kwargs["name"])
        if kwargs.get("description", ""):
            qs = qs.filter(description__contains=kwargs["description"])
        if kwargs.get("services", []):
            qs = qs.filter(services__pk__in=kwargs["services"])
        if kwargs.get("user", ""):
            qs = qs.filter(user=kwargs["user"])
        return qs


def validate_image(image):
    max_height = 320
    max_width = 320
    height = image.height
    width = image.width
    if width > max_width or height > max_height:
        raise ValidationError("Height or Width is larger than what is allowed")


class Provider(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="static/photos/",
        validators=[
            validate_image,
        ],
        blank=True,
        null=True,
    )
    thumbnail = models.ImageField(upload_to="static/thumbnails/", blank=True, null=True)

    objects = ProviderQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['pk']
