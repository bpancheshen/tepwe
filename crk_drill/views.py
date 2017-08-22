from django.views import generic
from django.core.urlresolvers import reverse_lazy
from crk_drill import forms
from crk_drill.models import Word


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
