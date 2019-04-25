from django.core.paginator import Paginator
from django.contrib import auth
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from asker.models import *
from asker.forms import *


def paginator(abstract_list, request):
    pager = Paginator(abstract_list, 4)

    page = request.GET.get('page')
    try:
        elements_on_page = pager.page(page)
    except:
        elements_on_page = pager.page(1)
    return elements_on_page


def index(request):
    question_list = Question.objects.get_new()
    question_list = paginator(question_list, request)

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


def logout(request):
    return redirect('/')


@login_required
def ask(request):
    # if request.POST:
    #     form = AskForm(
    #         request.user.profile,
    #         data=request.POST )
    #     if form.is_valid():
    #         q = form.save()
    #         return redirect(reverse(
    #             'question', kwargs={
    #                 'qid': q.pk
    #             }
    #         ))
    # else:
    #     form = AskForm(request.user.profile)
    return render(request, 'ask.html', {
        # 'form': form,
    })


def register(request):
    return render(request, 'signup.html', {})


def question(request, id):
    question_i = Question.objects.get(pk=id)
    answers = Answer.objects.get_hot(id)
    answers = paginator(answers, request)
    return render(request, 'question.html', {
        'answers': answers,
        'question': question_i,
    })


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    tag_i = Tag.objects.get(title=tag)
    questions_list = Question.objects.filter(tags=tag_i.id)
    questions_list = paginator(questions_list, request)

    return render(request, 'tag.html', {
        'questions': questions_list,
        'tag': tag,
    })




