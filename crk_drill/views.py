from django.views import generic
from django.core.urlresolvers import reverse_lazy
from crk_drill import forms
from crk_drill.models import Word, Lemma, Tag
from django.shortcuts import render

from django.http import HttpResponseRedirect

import random

class HomePage(generic.TemplateView):
    template_name = 'index.html'

class SignUp(generic.CreateView):
    form_class = forms.CreateUser
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class WordListView(generic.ListView):
    model=Word
    context_object_name = 'words'
    template_name = 'word_list.html'

#This, for now, is just a simple view that displays a question.
def QuestionView(request):
    #This needs to be a loop because some lemmas don't work with some tags.
    lemma = None
    wordform = None
    count = 0
    while wordform == None and count < 200:
        count += 1
        #look for a new lemma if one doesn't exist or we've already tried 10 times
        if lemma == None or count % 10 == 0:
        #pick a random lemma
            lemma_queryset = Lemma.objects.all()
            random_lemma_id = random.randint(0, len(lemma_queryset) - 1)
            lemma = lemma_queryset[random_lemma_id]

        #after you pick a lemma, it goes around again.
        else:
            #pick a random tag, appropriate for that lemma
                #some tinkering to get the appropriate fields
            pos = lemma.pos
            if pos == "N":
                animacy = lemma.trans_anim
                transitivity_animacy = ""
            elif pos == "V":
                animacy = ""
                transitivity_animacy = lemma.trans_anim

                #get a queryset
            tag_queryset = Tag.objects.filter(
                        pos=pos,
                        animacy=animacy,
                        transitivity_animacy=transitivity_animacy)

            #pick randomly
            random_tag_id = random.randint(0, len(tag_queryset) -1)
            tag = tag_queryset[random_tag_id]

            #assign a wordform, if there is exception, try again.
            try:
                wordform = Word.objects.filter(lemma=lemma, gram_code=tag)[0]
            except:
                wordform = None

    if request.method =="POST":
        form = forms.QuestionForm(request.POST, wordform)
        if form.is_valid():
            return HttpResponseRedirect('/question/')
    else:
        form = forms.QuestionForm(request.GET, wordform)
        print(form.field.label)


    return render(request, 'question_template.html', {'form':form})
