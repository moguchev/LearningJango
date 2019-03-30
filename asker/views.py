from django.shortcuts import render
from django.http import HttpResponse
from faker import Faker

fake = Faker()

def index(request):
    questions = [
        {
            'id': i,
            'title': fake.sentence(),
            'text' : '\n'.join(fake.sentences(fake.random_int(3, 6))),
            'tags' : [fake.word() for i in range(fake.random_int(2, 5))],
        }
        for i in range(5)
    ]
    return render(request, 'index.html', {
        'questions': questions,
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
    questions = [
        {
            'id': i,
            'title': fake.sentence(),
            'text': '\n'.join(fake.sentences(fake.random_int(3, 6))),
            'tags': [tag]
        }
        for i in range(5)
    ]
    return render(request, 'tag.html', {
        'questions': questions,
        'tag': tag,
    })
