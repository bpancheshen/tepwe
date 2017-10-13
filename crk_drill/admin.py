from django.contrib import admin
from .models import Word, Lemma,  Tag

# Register your models here.
admin.site.register(Word)
admin.site.register(Lemma)
admin.site.register(Tag)
