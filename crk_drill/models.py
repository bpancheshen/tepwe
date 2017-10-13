from django.db import models
from django.contrib import auth
from django.conf import settings
from django.forms import ModelForm
# Create your models here.

LEARNING_LANG = settings.LEARNING_LANG

class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return '@{}'.format(self.username)

class Word(models.Model):

    wordid = models.AutoField(primary_key=True)
    language = models.CharField(max_length=5, default=LEARNING_LANG, db_index=True)
    wordform = models.CharField(max_length=200, db_index=True)
    lemma = models.ForeignKey('Lemma', on_delete=models.CASCADE)
    #TODO change this to tag, you mess it up everytime.
    gram_code = models.ForeignKey('Tag', on_delete=models.CASCADE)
    translation = models.CharField(max_length=40, default="namôya nisitotin")

    def __str__(self):
        return self.wordform

    def is_noun(self):
        #TODO rewrite this and is_verb so it doesn't use the lemma variable.
        return self.lemma.pos=='N'

    def is_verb(self):
        return self.lemma.pos=='V'

class Lemma(models.Model):
#TODO: Make lemma a primary_key

    lemma = models.CharField(max_length=20)
    language = models.CharField(max_length=5, default=LEARNING_LANG)
    pos = models.CharField(max_length=12) # Accomodate larger PoS
    trans_anim = models.CharField(max_length=12)
    translation = models.CharField(max_length=40)

#This is unacceptable in this form. It's not needed yet, so I'm just commenting it out
    # course = models.ManyToManyField('Course')

    def __str__(self):
        return self.lemma

class Tag(models.Model):
    '''
    These tags are used by the fst to compute the forms.
    They will be different for every language and all must be included.
    For each field, the possible contents are defined in
    ../LANGCODE/meta/tags.txt
    for each here, the possible crk tags will be commented
    '''

    #the full string of the tag. Should be valid to the fst.
    string = models.CharField(primary_key=True, max_length=40, unique=True)
    pos = models.CharField(max_length=12)

    #only applies to nouns

    #AN or IN
    animacy = models.CharField(max_length=5, blank=True)
    #Sg or Pl
    number = models.CharField(max_length=5, blank=True)
    #Der/Dim or whether it's a diminutive or not
    derivation = models.CharField(max_length=7, blank=True)
    #Comp, Superl
    grade = models.CharField(max_length=10, blank=True)
    #Obv, Loc
    case = models.CharField(max_length=5, blank=True)

    #only applies to verbs

    #AI, II, TA, TI
    transitivity_animacy = models.CharField(max_length=5, blank=True)
    #Imp, Cnj, Ind, Cond
    mood = models.CharField(max_length=5, blank=True)
    #12Pl, 1Pl, 1Sg, etc
    personnumber = models.CharField(max_length=8, blank=True)
    #PV/e
    preverb = models.CharField(max_length=8, blank=True)
    #3SgO, 4SgO, 3PlO, etc, the personnumber of the object for TA verbs
    object = models.CharField(max_length=12, blank=True)
    #Neg
    polarity = models.CharField(max_length=5, blank=True)
    #Ind, Cnj
    mode = models.CharField(max_length=7, blank=True)
    #Prs, Prt, Fut
    tense = models.CharField(max_length=5, blank=True)
    #Def, Int
    intentional_definite = models.CharField(max_length=5, blank=True)


    connegative = models.CharField(max_length=5, blank=True)
    infinite = models.CharField(max_length=10, blank=True)

    # language = models.CharField(max_length=8)

    #applies to other parts of speech

    #Pos, I assume is possessive and not part of speech.
    attributive = models.CharField(max_length=5, blank=True)
    #Px12Pl, Px1Pl, Px2Pl.. etc
    possessive = models.CharField(max_length=10, blank=True)
    #Prox/Med/Dist
    distance = models.CharField(max_length=7, blank=True)
    #Prop, Pers, Dem, Interr, Refl, Card
    subclass = models.CharField(max_length=10, blank=True)

    #This model is from oahpa, these are forms that are not valid for crk
    gender = models.CharField(max_length=5, blank=True)
    language = models.CharField(max_length=5, blank=True)
    passive = models.CharField(max_length=5, blank=True)
    demtype = models.CharField(max_length=5, blank=True)
    reflexivepossessive = models.CharField(max_length=5, blank=True)
    punctuation = models.CharField(max_length=5, blank=True)
    #numbern and npxnumber are not in the db. go eat your hat.
    #pxcase1 through 3 are also not here. eat your socks too.
    numeraltype = models.CharField(max_length=5, blank=True)
    compound = models.CharField(max_length=5, blank=True)
    imptype = models.CharField(max_length=5, blank=True)
    syntax = models.CharField(max_length=5, blank=True)
    clitic = models.CharField(max_length=5, blank=True)
    nametype = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.string

"""
class Session(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"))
    question_list = models.CommaSeparatedIntegerField(
        max_length=1024, verbose_name=_("Question List"))


class Question(models.Model):
    wordform = models.ForeignKey(Word,
                                verbose_name=_("Wordform"),
                                blank=True,
                                null=True)
    tag = models.ForeignKey(Tag,
                                verbose_name=_("Tag"),
                                blank=True,
                                null=True)
    lemma = models.ForeignKey(Lemma,
                                verbose_name=_("Lemma"),
                                blank=True,
                                null=True)

    quiz = models.ManyToManyField(Quiz,
                                verbose_name=_("Quiz"),
                                blank=True)
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return str(self.wordform.wordform, self.tag.string)
"""
