# Generated by Django 3.1.3 on 2020-11-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20201108_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='payhistory',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]