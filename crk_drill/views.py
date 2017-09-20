from django.views import generic
from django.core.urlresolvers import reverse_lazy
from crk_drill import forms
from crk_drill.models import Word
from django.shortcuts import render

from django.http import HttpResponseRedirect


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
    if request.method =="POST":
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/question/')
    else:
        form = forms.QuestionForm()

    return render(request, 'question_template.html', {'form':form})
