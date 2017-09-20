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

class QuestionForm(forms.Form):
    #just query the database for the label
    wordform = None
    lemma = None
    count = 0
    #this may take a few tries, loop till you find one.
    while wordform == None and count < 100:
        count += 1
        #first you need a lemma
        if lemma == None:
            random_lemma_id = random.randint(0, Lemma.objects.count() - 1)
            lemma = Lemma.objects.filter(id=random_lemma_id)[0]

            #the loop is going to go around until it finds a lemma, then it executes the second part

        #then you need a Tag
        else:
            pos = lemma.pos

            #a little fiddling to get the parameter right.
            animacy = ''
            transitivity_animacy = ''
            if pos == "N":
                animacy = lemma.animacy
            elif pos == "V":
                transitivity_animacy = lemma.transitivity_animacy

            #GO FOR QUERY!!
            queryset_of_tags = Tag.objects.filter(
                                pos=pos,
                                animacy=animacy,
                                transitivity_animacy=transitivity_animacy)
            random_tag_id = randint(0, len(queryset_of_tags)-1)
            tag = queryset_of_tags[random_tag_id]
            #then you get the wordform for the lemma and tag,

    #define the label
    #define the answer.

    question = forms.CharField(label='question', max_length=50)
