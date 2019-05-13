from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Count
from django.utils import timezone
from asker.managers import *


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/%H',
        default='static/img/user.png',
        verbose_name='Avatar'
    )

    register_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Profile creation date'
    )

    rank = models.IntegerField(
        default=0,
        verbose_name='User rating')

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    objects = TagManager()
    title = models.CharField(max_length=32, verbose_name='Tag')

    def __str__(self):
        return self.title


class Like(models.Model):
    objects = LikeManager()

    VOTE_TYPES = [
        (1, 'LIKE'),
        (-1, 'DISLIKE')
    ]

    vote = models.SmallIntegerField(verbose_name='is like', default=VOTE_TYPES[0], choices=VOTE_TYPES)
    author = models.ForeignKey(
        to=Profile,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Like author',
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=-1)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Like from " + self.author.user.username


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(
        to=Profile,
        null=False,
        db_column="author",
        on_delete=models.PROTECT,
        verbose_name='Question author',
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Question date')
    title = models.CharField(max_length=128, verbose_name='Header')
    text = models.TextField(verbose_name='Question full text')

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Tags',
    )

    rating = models.IntegerField(default=0, null=False, verbose_name='Rating')
    votes = GenericRelation(Like, related_query_name='questions')

    def __str__(self):
        return f"{self.pk} {self.title}"


class Answer(models.Model):
    objects = AnswerManager()

    author = models.ForeignKey(
        to=Profile,
        null=False,
        verbose_name='Answer author',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(default=timezone.now)

    question = models.ForeignKey(
        to=Question,
        related_name='answers',
        verbose_name='Answered question',
        on_delete=models.CASCADE,
    )

    text = models.TextField(verbose_name='Answer full text')
    rating = models.IntegerField(default=0, null=False, verbose_name='Rate')
    votes = GenericRelation(Like, related_query_name='answers')

    def __str__(self):
        return self.text