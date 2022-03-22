# Generated by Django 2.2.2 on 2022-03-20 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceTypeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type_name', models.CharField(max_length=255)),
                ('rate', models.CharField(max_length=100, null=True)),
                ('in_effect', models.BooleanField(default=True)),
                ('studio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receive_date', models.DateField(null=True)),
                ('note', models.TextField(max_length=2024, null=True)),
                ('image', models.ImageField(null=True, upload_to='studio/requests')),
                ('print_status', models.CharField(choices=[('0', 'Pending'), ('1', 'Received'), ('2', 'Printed'), ('3', 'Cancelled')], default='0', max_length=1)),
                ('request_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('service_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.ServiceTypeModel')),
                ('studio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='studio', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
