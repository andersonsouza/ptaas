# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.hashers import make_password


def initial_setup_user(apps, schema_editor):
    User = apps.get_registered_model('auth', 'User')
    admin = User(
         username='admin',
         email='admin@localhost',
         password=make_password('admin'),
         is_superuser=True,
         is_staff=True
    )
    admin.save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(initial_setup_user),
    ]
