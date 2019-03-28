from django.shortcuts import render
from django.http import HttpResponse


def index(request) :
    questions = [
        { 'id' : i, 'title' : f'Question #{i}'}
        for i in range(3)
    ]
    return render(request, 'index.html', {
        'questions' : questions,
    })

def login(request) :
    return render(request, 'login.html', {})

def ask(request) :
    return render(request, 'ask.html', {})

def register(request) :
    return render(request, 'signup.html', {})

def question(request, id) :
    return render(request, 'question.html', {})

def settings(request) :
    return render(request, 'settings.html', {})

def tag(request) :
    return render(request, 'tag.html', {})