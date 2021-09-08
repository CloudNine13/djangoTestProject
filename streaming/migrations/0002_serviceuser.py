# Generated by Django 3.2.6 on 2021-09-08 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('streaming', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
