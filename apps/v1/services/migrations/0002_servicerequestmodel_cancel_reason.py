# Generated by Django 2.2.2 on 2022-03-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequestmodel',
            name='cancel_reason',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
