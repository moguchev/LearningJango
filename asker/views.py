from django.shortcuts import render
from django.http import HttpResponse
from faker import Faker
from django.core.paginator import Paginator


fake = Faker()
questions = [
        {
            'id': i,
            'title': fake.sentence(),
            'text': '\n'.join(fake.sentences(fake.random_int(3, 6))),
            'tags': [fake.word() for i in range(fake.random_int(2, 5))],
        }
        for i in range(50)
    ]


def paginator(questions_list, request):
    pager = Paginator(questions_list, 4)

    page = request.GET.get('page')
    try:
        questions_on_page = pager.page(page)
    except:
        questions_on_page = pager.page(1)
    return questions_on_page


def index(request):
    questions_list = paginator(questions,request);

    return render(request, 'index.html', {
        'questions': questions_list,
    })


def login(request):
    return render(request, 'login.html', {})


def ask(request):
    return render(request, 'ask.html', {})


def register(request):
    return render(request, 'signup.html', {})


def question(request, id):
    return render(request, 'question.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    tag_questions = [
        {
            'id': i,
            'title': fake.sentence(),
            'text': '\n'.join(fake.sentences(fake.random_int(3, 6))),
            'tags': [tag]
        }
        for i in range(8)
    ]
    questions_list = paginator(tag_questions, request)

    return render(request, 'tag.html', {
        'questions': questions_list,
        'tag': tag,
    })


def hot(request):
    hot_questions = [
        {
            'id': i,
            'title': fake.sentence(),
            'text': '\n'.join(fake.sentences(fake.random_int(3, 6))),
            'tags': [fake.word() for i in range(fake.random_int(2, 3))],
        }
        for i in range(8)
    ]
    questions_list = paginator(hot_questions, request)

    return render(request, 'hot.html', {
        'questions': questions_list,
    })

