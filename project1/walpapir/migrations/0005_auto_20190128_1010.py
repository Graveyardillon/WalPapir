# Generated by Django 2.1.4 on 2019-01-28 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walpapir', '0004_auto_20190126_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='description',
            new_name='self_introduction',
        ),
    ]