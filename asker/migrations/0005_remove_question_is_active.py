# Generated by Django 2.1.7 on 2019-05-11 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0004_auto_20190507_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_active',
        ),
    ]
