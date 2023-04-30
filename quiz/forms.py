from django import forms
from .models import User, Quiz
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in ["username", "password1", "password2"]:
            self.fields[field].help_text = None
            self.fields['first_name'].label = 'Name'
            self.fields['first_name'].required = True

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ['authored_by',]
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ''
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'special special_big', 'placeholder':'Quiz Title'}))


class QuestionForm(forms.Form):
    quiz = forms.UUIDField(widget=forms.HiddenInput())
    question = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'special', 'placeholder':'Question'}))
    option_1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'special special_small', 'placeholder':'Option A'}))
    option_2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'special special_small', 'placeholder':'Option B'}))
    option_3 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'special special_small', 'placeholder':'Option C'}))
    correct_answer = forms.ChoiceField(choices=[(1, 'A'), (2, 'B'), (3, 'C')], widget=forms.RadioSelect(attrs={'class':'radio-inline', 'required':True}))

    
