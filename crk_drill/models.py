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
    gram_code = models.CharField(max_length=40, default='null')
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
    animacy = models.CharField(max_length=20)

    def __str__(self):
        return self.lemma
