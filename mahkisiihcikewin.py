# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:59:36 2017

@author: Brent

mahkisîhcikêwin (VII) means something is expanding. 

This script takes the list of lemmas and expands them so that the database
includes every word form for that lemma. 

NOTE: If you are not using the giellatechno fst, redefine fstResults()
"""

import os, requests, bs4

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crk_oapha.settings")

import django
django.setup()

from crk_drill.models import Word, Lemma

#Name of the CSV file which contains the database contents for crk_drill_lemma
#IMPORTANT first line should be field names.
CSV_LEMMA = 'crk_drill_lemma.csv'

FST_PRETEXT = "http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text="
FST_POSTTEXT = "&pos=Any&mode=full&lang=crk&plang=eng&action=paradigm"

def main():
    #get the csv file for crk_drill_lemmas
    lemmas, fields , lemma_dictionary = loadFile()
    print(lemma_dictionary)
    #for each lemmma, query the finite state transducer(fst), add the form to wordforms
    wordforms= []
    for l in lemmas:
        the_table = fstResults(l)
        for row in the_table:
            wordforms.append(parse_row(row))
            
    for word_set in wordforms:
        lemma, lemma_created = Lemma.objects.get_or_create(lemma=word_set[0])
        entry, created = Word.objects.get_or_create(
            wordform=word_set[2], 
            lemma=lemma,    #should link to the id of the lemma
            gram_code =word_set[1]
        )
        
        #print some stuff letting the user know whats going on
        if created:
            print(word_set[2] + " was added to database.")
            
        else:
            print(word_set[2] + " failed.")
        
    #with the query, create a csv file that contains every wordform

def loadFile():
    """
    opens the exported db file described as CSV_LEMMA, 
    then returns a list of each lemma in the table
    and a list of all the columns in the database table.
    """
    #each line of the crk_drill_lemmas
    lines = open(CSV_LEMMA, 'r', encoding='utf8').readlines()
    
    #first line is a list of fields
    fields = []
    #some formatting
    header = lines[0]
    header = header.replace('"', '')    #get rid of quotes
    header = header.strip()             #get rid of newline
    header = header.split(',')          #make into a list
    
    for e in header:
        fields.append( e)
    
    #which field is lemma?
    l_field = 0
    for i in range(len(fields)):
        if 'lemma' in fields[i]:
            l_field = i
        
    #all lemmas in crk_drill_lemmas
    lemmas = []
    lemma_dictionary = {}
    for line in lines[1:]:
        line = line.strip()
        line = line.replace('"','').split(',')
        
        entry = line[l_field]
        lemmas.append(entry)
        #add an entry into the dictionary, this will link the lemma id with the word id
        lemma_dictionary[entry] = line[0]
        
    return lemmas, fields, lemma_dictionary

def fstResults(l):
    """
    This only works for giellatechnos fst form. 
    set where to get the site in the following variables, PRETEXT is everything before 
    the query word. POSTTEXT is everything after.
    Redefine this method if you are not using the website.
    """
    
    FST_PRETEXT = "http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text="
    FST_POSTTEXT = "&pos=Any&mode=full&lang=crk&plang=eng&action=paradigm"

    
    #query the page
    page = requests.get(FST_PRETEXT + l + FST_POSTTEXT)
    
    #make some beautful soup
    page_bs4 = bs4.BeautifulSoup(page.text.encode('utf-8'), "lxml")

    
    page_bs4.table.extract()
    if page_bs4.table != None:
        return page_bs4.table.find_all('tr')
        
    else:
        print('Did not find table for ' + l)
        
def parse_row(table_row):
    #use beautiful soup
#    row_bs4 = bs4.BeautifulSoup(table_row, 'lxml')
#    print(table_row)
    
    #parse stem
    stem = table_row.td.extract().get_text()
    stem = ''.join(stem.split('\n'))
    
    #parse grammar code
    gram_code = table_row.td.extract().get_text()
    gram_code = str(gram_code).replace(' ', '+')
    
    #parse wordform
    wordform = table_row.td.extract().get_text()
    wordform = ''.join(wordform.split('\n'))
    
    return [stem, gram_code, wordform]
    

if __name__ == "__main__": main()
