# Generated by Django 4.1.5 on 2024-02-19 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_result'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]