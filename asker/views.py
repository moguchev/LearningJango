from django.core.paginator import Paginator
from django.utils.http import is_safe_url, urlunquote
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from asker.models import *
from asker.forms import *
from django.db import models

def paginator(abstract_list, request):
    pager = Paginator(abstract_list, 4)

    try:
        page = int(request.GET.get('page', 1))
        elements_on_page = pager.page(page)
    except:
        elements_on_page = pager.page(1)
    return elements_on_page


def index(request):
    question_list = Question.objects.get_new()
    question_list = paginator(question_list, request)
    question_list = question_list.object_list.annotate(num_answers=Count('answers'))

    return render(request, 'index.html', {
        'questions': question_list,
        'indexPage': True,
    })


def hot(request):
    questions_list_hot = Question.objects.get_hot()
    questions_list_hot = paginator(questions_list_hot, request)

    return render(request, 'index.html', {
        'questions': questions_list_hot,
        'indexPage': False,
    })


def tag(request, tag):
    tag_i = Tag.objects.get(title=tag)
    questions_list = Question.objects.filter(tags=tag_i.id)
    questions_list = paginator(questions_list, request)

    return render(request, 'tag.html', {
        'questions': questions_list,
        'tag': tag,
    })


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = auth.authenticate(**cdata)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            form.add_error(None, "no such user")
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
    })


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def ask(request):
    if request.POST:
        form = AskForm(
            request.user.profile,
            data=request.POST
        )
        if form.is_valid():
            q = form.save()
            return redirect(reverse(
                'question', kwargs={
                    'id': q.pk
                }
            ))
    else:
        form = AskForm(request.user.profile)
    return render(request, 'ask.html', {
        'form': form,
    })


def register(request):
    if request.POST:
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
        auth.logout(request)
    return render(request, 'signup.html', {
        'form': form
    })


def question(request, id):
    question_i = Question.objects.get(pk=id)
    tags = question_i.tags.all()
    if request.POST:
        if request.user.is_anonymous:
            return redirect(reverse('login'))

        form = AnswerForm(
            request.user,
            id,
            data=request.POST
        )
        if form.is_valid():
            answer = form.save()
            answer.save()
            return redirect(reverse(
                'question', kwargs={
                    'id': id
                }
            ))
    else:
        form = AnswerForm(request.user, id)

    answers = Answer.objects.get_hot(id)
    answers = paginator(answers, request)
    return render(request, 'question.html', {
        'question': question_i,
        'answers': answers,
        'tags': tags,
        'form': form
    })


@login_required
def settings(request):
    user = request.user
    if request.POST:
        form = SettingsForm()
        #if form.is_valid():

    else:
        form = SettingsForm()
        return render(request, 'settings.html', {
            'profile': user,
            'form': form
        })






