from django import forms
from asker.models import Question


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cdata = super().clean()

        pass_one = cdata.get('password1')
        pass_two = cdata.get('password1')
        if pass_one != pass_two:
            raise forms.ValidationError()


    #def clean_username(forms.Form):
     #   username = self.

# class AskForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['title', 'text']
#
#     def __init__(self, profile, *args, **kwargs):
#         self.profile = profile
#         super().__init__(args, **kwargs)
#
#     def save(self, commit=True):
#         if self.is_valid():
#             cdata = self.cleaned_data
#             question = Question(**cdata)
#             question.author = self.profile
#             if commit:
#                 question.save()
#             return question
