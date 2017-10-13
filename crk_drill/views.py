from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from crk_drill import forms
from crk_drill.models import Word, Lemma, Tag
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse

from random import choice

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

class QuestionView(generic.FormView):
    form_class = forms.BasicLeksaForm
    template_name = "question_template.html"

    def form_valid(self, form):
        guess = form.cleaned_data['answer']

        # for thing in self.request.POST.items():
        #     print(thing)
        lemma = self.request.POST.get('lemma')

        lemmaObject = Lemma.objects.get(lemma=lemma)

        if guess == lemmaObject.translation:
            return HttpResponseRedirect(reverse('questionview'))
        else:
            return HttpResponse("You're wrong.")



    #prepare the form! find the lemma and tag
    # def get_form(self):
        # print("running get_form")
        # form_class=self.form_class
        # if self.request.method == "GET":
            # lemma = get_leksa_lemma()
            # self.lemma = lemma
        # else:
        #     self.lemma = self.request.POST["lemma"]
        #     self.tag = self.request.POST["tag"]
        # return form_class(**self.get_form_kwargs())

    #Hi Frodo, This is how we pass kwargs to the form instantiation.
    def get_form_kwargs(self):
        print("running get_form_kwargs")
        kwargs = super(QuestionView, self).get_form_kwargs()



        return dict(kwargs)

    def get_context_data(self, **kwargs):
        print("running get context data")
        self.lemma = get_leksa_lemma()
        print(self.lemma.translation)

        context =  super(QuestionView, self).get_context_data(**kwargs)

        context["lemma"] = self.lemma
        print(context['lemma'])
        return context

def get_leksa_lemma():
    """
        This is for debugging and testing. It's not a real system. Delete this when
        Courses are functioning.

        @returns a lemma object

    """
    return choice(Lemma.objects.all())

def get_lemma_and_tag():
    """
    This is for debugging and testing. It's not a real system. Delete this when
    Courses are functioning.

    @returns a tuple containing randomLemma, randomTag

    First it finds a wordform, then uses the associated tag and lemma
    """

    returnTag = None
    returnLemma = None

    #for testing purposes, this is really really limited. models.py needs to be
    #changed to make this less cumbersome.
    poss_animacy = ['AN', 'IN']
    poss_tags = {"AN":
                ["N+AN+Pl", "N+AN+Sg", "N+AN+Loc"],
                "IN":
                ["N+IN+Pl", "N+IN+Sg", "N+IN+Loc"],
                }
    pick_a_tag = choice(poss_tags[choice(poss_animacy)])

    #find your wordform
    form = choice(Word.objects.filter(gram_code=pick_a_tag))

    #determine your tags and lemmas from the wordform. Then, forget about the form.
    returnTag = form.gram_code
    returnLemma = form.lemma
    print(form.wordform)

    return returnLemma, returnTag

    # while returnTag == None and count<100:
    #     if returnLemma == None or count%10 == 0:
    #         #get the number of lemmas in the database
    #         num_of_lemmas = Lemma.objects.count()
    #         #a random integer from 1 to the total number of lemmas.
    #         ran_num = random.randint(1, num_of_lemmas)
    #         #try for that lemma
    #         try:
    #             returnLemma = Lemma.objects.get(pk=ran_num)
    #             print("found a lemma,", returnLemma.lemma, ran_num)
    #         except:
    #             print("From within get_lemma_and_tag(), couldn't find lemma number ",
    #                 ran_num)
    #
    #
    #     #get the number of pos and animacy
    #     pos = returnLemma.pos
    #     #make a dictionary that will be used to lookup valid tags
    #     kwarg_dict = {"pos":pos}
    #     animacy = returnLemma.trans_anim
    #     if pos == "N":
    #         kwarg_dict["animacy"] = animacy
    #     if pos == "V":
    #         kwarg_dict["transitivity_animacy"] = animacy
    #
    #
    #     possible_tags = Tag.objects.filter(**kwarg_dict)
    #     #a random int
    #     maybe_this_tag = random.choice(possible_tags)
    #     print("trying tag", maybe_this_tag.string)
    #     try:
    #         returnTag = Tag.objects.get(pk=maybe_this_tag.string)
    #         print("found a tag")
    #     except:
    #         pass
    #
    #     #now, check to see that there is a wordform
    #     try:
    #         testForm = Form.objects.get(lemma=returnLemma, tag=returnTag)
    #     #if it doesn't return a queryset, it's a fail and loop again.
    #     except:
    #         returnTag = None
    #     count += 1
    #
    # return returnLemma, returnTag

# #This, for now, is just a simple view that displays a question.
# def QuestionView(request):
#     #This needs to be a loop because some lemmas don't work with some tags.
#     lemma = None
#     wordform = None
#     count = 0
#     while wordform == None and count < 200:
#         count += 1
#         #look for a new lemma if one doesn't exist or we've already tried 10 times
#         if lemma == None or count % 10 == 0:
#         #pick a random lemma
#             lemma_queryset = Lemma.objects.all()
#             random_lemma_id = random.randint(0, len(lemma_queryset) - 1)
#             lemma = lemma_queryset[random_lemma_id]
#
#         #after you pick a lemma, it goes around again.
#         else:
#             #pick a random tag, appropriate for that lemma
#                 #some tinkering to get the appropriate fields
#             pos = lemma.pos
#             if pos == "N":
#                 animacy = lemma.trans_anim
#                 transitivity_animacy = ""
#             elif pos == "V":
#                 animacy = ""
#                 transitivity_animacy = lemma.trans_anim
#
#                 #get a queryset
#             tag_queryset = Tag.objects.filter(
#                         pos=pos,
#                         animacy=animacy,
#                         transitivity_animacy=transitivity_animacy)
#
#             #pick randomly
#             random_tag_id = random.randint(0, len(tag_queryset) -1)
#             tag = tag_queryset[random_tag_id]
#
#             #assign a wordform, if there is exception, try again.
#             try:
#                 wordform = Word.objects.filter(lemma=lemma, gram_code=tag)[0]
#             except:
#                 wordform = None
#
#     if request.method =="POST":
#         form = forms.QuestionForm(request.POST, wordform)
#         if form.is_valid():
#             return HttpResponseRedirect('/question/')
#     else:
#         form = forms.QuestionForm(request.GET, wordform)
#         print(form.field.label)
#
#
#     return render(request, 'question_template.html', {'form':form})
