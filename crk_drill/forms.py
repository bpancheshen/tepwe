from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms

from crk_drill.models import Lemma, Tag, Word
from crk_drill.models import QuestionForm
import random

class CreateUser(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2',)
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = "Email Address"

class QuestionForm(forms.Form):
    
    def __init__(self, data, wordform, *args, **kwargs):
        self.wordform = wordform
        self.field = forms.CharField(
                label = wordform.wordform + " " + wordform.gram_code.string,
                max_length=50)

        return super(QuestionForm, self).__init__(data, *args, **kwargs)
