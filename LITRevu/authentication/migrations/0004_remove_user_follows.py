# Generated by Django 5.2.1 on 2025-06-06 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
    ]
