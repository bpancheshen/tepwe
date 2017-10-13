from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms

from crk_drill.models import Lemma, Tag, Word
import random

class CreateUser(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2',)
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = "Email Address"

class BasicLeksaForm(forms.Form):
    answer = forms.CharField(max_length=40, label="Translation")




    # def clean_answer(self):
    #     # print("cleaning answer")
    #     #oh, you're ready to check the answer,
    #     #well,
    #     #you're going to need the answer from request.POST
    #     answer = self.cleaned_data.get('answer')
    #
    #     lemma = self.cleaned_data.get('lemma')
    #
    #     print(lemma, tag)
    #
    #     #check it against the form
    #     correct_answer = Lemma.objects.get(lemma='lemma')
    #     print(answer)
    #     print(correct_answer)
    #
    #     if answer != correct_answer:
    #         raise forms.ValidationError(self.error_messages['incorrect_answer'],
    #             code='incorrect_answer')
    #     return answer
