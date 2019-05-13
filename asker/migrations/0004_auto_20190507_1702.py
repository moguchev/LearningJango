# Generated by Django 2.1.7 on 2019-05-07 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0003_auto_20190427_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='upload',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='static/img/user.png', upload_to='avatars/%Y/%m/%d/%H', verbose_name='Avatar'),
        ),
    ]
