from django.db import models
from django.contrib.auth.models import UserManager
from django.db.models import Sum


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.all().order_by('-rating').prefetch_related()

    def get_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title).prefetch_related()

    def get_new(self):
        return self.all().order_by('-created_at').prefetch_related()

    def get_by_id(self, qid):
        return self.all().filter(id=qid)


class AnswerManager(models.Manager):
    def get_hot(self, qid):
        return self.filter(question=qid).order_by('-rating').prefetch_related()


class TagManager(models.Manager):
    def by_tag(self, tag_str):
        return self.filter(title=tag_str).first().questions.all().order_by('-created_at').reverse()


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0
