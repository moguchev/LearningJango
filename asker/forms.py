from django import forms
from asker.models import Question
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import *
from django.core import validators
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Login'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError('Incorrect login or password')


class TagField(forms.Field):
    @classmethod
    def get_tags(cls, tags):
        if tags in validators.EMPTY_VALUES:
            return []

        tags = [item.strip() for item in tags.split(',') if item.strip()]
        return tags

    def clean(self, tags):
        tags = self.get_tags(tags)
        self.validate(tags)
        self.run_validators(tags)
        return tags


class AskForm(forms.ModelForm):
    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'text']

    title = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Title'
    }))
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Question',
        'rows': 15
    }))
    tags = TagField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Enter tags separate by comma'
    }))

    def save(self, commit=True):
        data = self.cleaned_data
        profile_id = User.objects.get(id=self.profile.pk).profile.id
        question = Question(
            title=data['title'],
            text=data['text'],
            author_id=profile_id
        )
        question.save()
        tags = data['tags']
        for t in tags:
            tag = Tag.objects.get_or_create(title=t)[0]
            question.tags.add(tag)
        question.save()

        return question


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Dr_peper'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'mymail@mail.ru'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Password'
    }))

    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Repeat password'
    }))

    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control input-lg'
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Login is already exists!')
        return username

    def clean_repeat_password(self):
        data = self.cleaned_data
        if data['password'] != data['repeat_password']:
            raise forms.ValidationError('Different passwords!')
        return data['repeat_password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email is already exists!')
        return email

    def save(self, commit=True):
        data = self.cleaned_data
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        if self.cleaned_data['avatar'] is not None:
            profile = Profile(user=user, avatar=self.cleaned_data['avatar'])
            profile.save()
            user.save()
        else:
            profile = Profile(user=user)
            profile.save()
            user.save()
        return user


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'Enter your answer here',
        'rows': 5,
    }))

    def __init__(self, user, question_id, *args, **kwargs):
        if user.is_anonymous:
            self.profile = None
        else:
            self.profile = user.profile
        self.question_id = question_id
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        data = self.cleaned_data
        profile_id = User.objects.get(id=self.profile.pk).profile.id
        answer = Answer.objects.create(
            author_id=profile_id,
            question_id=self.question_id,
            text=data['text'],
            rating=0
        )
        answer.save()

        return answer


class SettingsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input-lg',
    }))

    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control input-lg',
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.fields['username'].has_changed(initial=self.initial['username'], \
                                               data=username):
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Login already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.fields['email'].has_changed(initial=self.initial['email'], \
                                            data=email):
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists!')
        return email

    def save(self, user):
        data = self.cleaned_data
        user.username = data['username']
        user.email = data['email']
        if data['avatar'] is not None:
            user.avatar = data['avatar']
        user.save()
