# Generated by Django 3.2.6 on 2021-09-08 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0002_serviceuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceuser',
            name='stripeCustomerId',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serviceuser',
            name='stripeSubscriptionId',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
