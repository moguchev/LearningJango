from django.contrib.auth.models import UserManager as AbstractUserManager
from django.db import models
from django.db.models import Sum


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.filter(is_active=True).order_by('-rating').prefetch_related()

    def get_by_tag(self, tag_title):
        return self.filter(is_active=True).filter(tags__title=tag_title).prefetch_related()

    def get_new(self):
        return self.all().order_by('-created_at').prefetch_related()

    def get_by_id(self, qid):
        return self.all().filter(id=qid)


class AnswerManager(models.Manager):
    def get_hot(self):
        return self.all().order_by('-rating').reverse()


class TagManager(models.Manager):
    def by_tag(self, tag_str):
        return self.filter(title=tag_str).first().questions.all().order_by('-created_at').reverse()


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


