# Generated by Django 2.1.7 on 2019-04-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='answer',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='upload',
            field=models.ImageField(default='img/test.png', upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='asker.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=32, verbose_name='Tag'),
        ),
    ]
