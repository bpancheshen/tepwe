from django.db import models
from django.contrib import auth
from django.conf import settings
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
    gram_code = models.ForeignKey('Tag', on_delete=models.CASCADE)
    translation = models.CharField(max_length=40)

    def __str__(self):
        return self.wordform

    def is_noun(self):
        #TODO rewrite this and is_verb so it doesn't use the lemma variable.
        return self.lemma.pos=='N'

    def is_verb(self):
        return self.lemma.pos=='V'

class Lemma(models.Model):

    lemma = models.CharField(max_length=20)
    language = models.CharField(max_length=5, default=LEARNING_LANG)
    pos = models.CharField(max_length=12) # Accomodate larger PoS

    course = models.ManyToManyField(Course)

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
    string = models.CharField(max_length=40, unique=True)
 	pos = models.CharField(max_length=12)

    #only applies to nouns

    #AN or IN
 	animacy = models.CharField(max_length=5)
    #Sg or Pl
 	number = models.CharField(max_length=5)
    #Der/Dim or whether it's a diminutive or not
 	derivation = models.CharField(max_length=7)
    #Comp, Superl
 	grade = models.CharField(max_length=10)
    #Obv, Loc
    case = models.CharField(max_length=5)

    #only applies to verbs

    #AI, II, TA, TI
 	trans_anim = models.CharField(max_length=5)
    #Imp, Cnj, Ind, Cond
 	mood = models.CharField(max_length=5)
    #12Pl, 1Pl, 1Sg, etc
    personnumber = models.CharField(max_length=8)
    #PV/e
 	preverb = models.CharField(max_length=8)
    #3SgO, 4SgO, 3PlO, etc, the personnumber of the object for TA verbs
 	object = models.CharField(max_length=12)
    #Neg
 	polarity = models.CharField(max_length=5)
    #Ind, Cnj
 	mode = models.CharField(max_length=7)
    #Prs, Prt, Fut
 	tense = models.CharField(max_length=5)
    #Def, Int
    intentional_definite = models.CharField(max_length=5)


 	# conneg = models.CharField(max_length=5)
 	infinite = models.CharField(max_length=10)

 	# language = models.CharField(max_length=8)

    #applies to other parts of speech

    #Pos, I assume is possessive and not part of speech.
 	attributive = models.CharField(max_length=5)
    #Px12Pl, Px1Pl, Px2Pl.. etc
 	possessive = models.CharField(max_length=10)
    #Prox/Med/Dist
 	distance = models.CharField(max_length=7)
    #Prop, Pers, Dem, Interr, Refl, Card
 	subclass = models.CharField(max_length=10)

    #This model is from oahpa, these are forms that are not valid for crk
 	gender = models.CharField(max_length=5)

    def __str__(self):
        return self.string

class Course(models.Model):

    teacher = models.CharField(max_length=50)
    #also courses should have a list of words.
    lemmas = models.ManyToManyField(Lemma)
