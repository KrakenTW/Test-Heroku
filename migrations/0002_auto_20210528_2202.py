# Generated by Django 3.2.3 on 2021-05-28 22:02

from django.db import migrations, models
import providers.models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/photos/', validators=[providers.models.validate_image]),
        ),
        migrations.AddField(
            model_name='provider',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='static/thumbnails/'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
