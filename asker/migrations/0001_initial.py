# Generated by Django 2.1.7 on 2019-04-15 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(verbose_name='Answer full text')),
                ('rating', models.IntegerField(default=0, verbose_name='Rate')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.SmallIntegerField(choices=[(1, 'LIKE'), (-1, 'DISLIKE')], default=(1, 'LIKE'), verbose_name='is like')),
                ('object_id', models.PositiveIntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(default='avatars/emptyUser.png', upload_to='uploads/%Y/%m/%d/')),
                ('register_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Profile creation date')),
                ('rank', models.IntegerField(default=0, verbose_name='User rating')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Question date')),
                ('title', models.CharField(max_length=128, verbose_name='Header')),
                ('text', models.TextField(verbose_name='Question full text')),
                ('is_active', models.BooleanField(default=True)),
                ('rating', models.IntegerField(default=0, verbose_name='Rating')),
                ('author', models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.PROTECT, to='asker.Profile', verbose_name='Question author')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='404', max_length=32, verbose_name='Tag')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='questions', to='asker.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='like',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='asker.Profile', verbose_name='Like author'),
        ),
        migrations.AddField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asker.Profile', verbose_name='Answer author'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='asker.Question', verbose_name='Answered question'),
        ),
    ]
