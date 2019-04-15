from django.contrib import admin
from asker.models import Profile, Question, Tag, Like, Answer


admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)
admin.site.register(Profile)