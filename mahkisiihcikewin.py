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
import subprocess as sp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crk_oapha.settings")

import django
django.setup()

from crk_drill.models import Word, Lemma, Tag

#Name of the CSV file which contains the database contents for crk_drill_lemma
#IMPORTANT first line should be field names.
CSV_LEMMA = 'crk_drill_lemma.csv'

#This is the file that contains all the paradigms for the languages
PARADIGM_FILE = 'paradigms.txt'

#Here is the command that activates the generator
GEN_COMMAND = ['lookup', '-q', '-flags', 'mbTTx', '/home/brent/main/langs/crk/src/generator-gt-norm.xfst']
#hfst version
# GEN_COMMAND = ['hfst-lookup', '-q', '~/main/langs/crk/src/analyser-gt-norm.hfstol']

#These variables are for if you are extracting wordforms from the giellatechno
#website. This method is unfinished and will not work. I started using FSTs
#on my own computer to build the database.
USE_GT = False
FST_PRETEXT = "http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text="
FST_POSTTEXT = "&pos=Any&mode=full&lang=crk&plang=eng&action=paradigm"


#A list of tagsets used to develope and debug the program
taggy_tags = ["N+AN+Sg", "N+AN+Pl"]
def main(USE_GT):
    if USE_GT:
        #get the csv file for crk_drill_lemmas
        lemmas, fields , lemma_dictionary = loadFile()
        print(lemma_dictionary)
        #for each lemmma, query the finite state transducer(fst), add the form to wordforms
        wordforms= []
        for l in lemmas:
            the_table = GT_fstResults(l)
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
    else:
        """
        Do this if you're using the transducers on your own machine.
        """
        #load that FILE!!!
        lemmas, fields , lemma_dictionary = loadFile()

        #load tag file
        tag_dictionary = load_tagfile()

        #get your tagsets from paradigm.txt
        allTags = Tagset(PARADIGM_FILE)

        # tags.paradigmDict['N+AN']

        #This is how you call the queryGenerator
        # output, err = queryGenerator('atim', "N+AN+Pl")
        # print(output)

        # TODO check to see if all the lemmas are already in the database,
            #if they aren't in the database, add the lemmas

        for l in lemmas:
            #make sure that at least one wordform is created for the lemma
            found_one = False

            #get the string of the lemma i.e. 'atim'
            lemmaForm = l[0]
            #get the type of word. i.e. "N+AN", or "V+TI"
            lemmaType = l[1]
            translation = l[2]
            lemma_object, lemma_created = Lemma.objects.get_or_create(
                                            lemma = lemmaForm,
                                            pos = lemmaType.split('+')[0],
                                            trans_anim = lemmaType.split('+')[1])

            #run the generator for each tag appropriate for this lemmaType
            for tag in allTags.paradigmDict[lemmaType]:

                #query the fst only if the wordform is new.
                #TODO find a way to look for an object without throwing an error upon failure.
                try:
                    already_a_word = Word.objects.get(lemma=lemma_object, gram_code=tag)
                except:
                    already_a_word = False
                #if already_a_word is an object or if it's true, flip the variable
                #so an error message is not sent.
                if already_a_word != False:
                    # print('no query for ' + lemmaForm, tag)
                    found_one = True

                else:
                    output, err = queryGenerator(lemmaForm, tag)

                    if err:
                        print("WARNING: ERROR on" + lemmaForm, tag)

                    #this option means the fst didn't generate a form
                    elif output.strip().endswith('+?'):
                        # print(tag, "not found for", lemmaForm)
                        pass

                    #everything is good, lets continue.
                    else:
                        found_one = True

                        #a little formatting.
                        #   sometimes there is more than one form. Output looks like this
                        #   '\tkititwânânaw\n\tkititwânaw\n\n'
                        output = output.split()

                        #parse tags to add it to the database
                        #The tag are set up down here instead of in their own method
                        #because I only want tags that are useful in the database.
                        # print('attempting to add ' + tag + ' for ' + lemmaForm)
                        tag_object, tag_created = add_tags_to_db(
                                                                tag,
                                                                tag_dictionary)



                        word_object, word_created = Word.objects.get_or_create(
                                                    wordform=output[0], #TODO add all the wordforms
                                                    lemma=lemma_object,
                                                    gram_code=tag_object,)
                        if word_created:
                            # print('wordform was created for: ', lemmaForm, tag)
                            pass
                        else:
                            print('word object already exists for :', lemmaForm, tag)

            if not found_one:
                print(lemmaForm + " produced not even a single lem. !!ALERT!!")
                the_pause = input("hit enter to acknowledge")

def loadFile():
    """
    opens the exported db file described as CSV_LEMMA,
    then returns a list of tuples (lemma, lemma_type),
     a list of all the columns in the database table,
     and a dictionary thats keys are lemmas and values are lemma id values from
     the database.

     In order for this to happen correctly, the csv file needs to be exported
     with first row containing column names.

     ex.

     lemmas, fields, dict = loadFile()
     lemmas[0] = ('atim', 'N+AN', 'dog')
     fields[0] = lemma_id
     dictionary[atim] = 1

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

        #get the lemma
        entry = line[l_field]

        #get the lemma type
        lemma_type = line[3] + "+" + line[4]

        translation = line[5]

        #append the list to be returned with a tuple of the lemma and it's type.
        lemmas.append((entry, lemma_type, translation))

        #add an entry into the dictionary, this will link the lemma id with the word id
        lemma_dictionary[entry] = line[0]

    return lemmas, fields, lemma_dictionary
def load_tagfile():
    """
    This loads the file tags.txt. It parses it and stores it as a dictionary.
    keys are tags, values are their associated model field. This way no linguistics
    info is hardcoded into the program.
    """
    #load tags.txt, it's used to determine which tags fall under which model fields.
    tags_and_headings = open('tags.txt', 'r', encoding='utf-8').readlines()
    #create a dictionary, keys are tags, values are the name of the model field
    fieldmap = {}
    heading = ''
    for line in tags_and_headings:
        #get rid of those pesky new line characters
        line = line.strip()

        if line.startswith('#'):
            line = line.strip('#')
            heading = line
        #there are some duplicate tags. I don't want them. Only add to fieldmap
        #if the tag is unique
        elif line not in fieldmap:
            # print('adding to fieldmap: ',line, heading.lower() )
            fieldmap[line] = heading.lower()
            # print (fieldmap[line])

    return fieldmap

def add_tags_to_db(tag, fieldmap):
    """
    This accepts the argument, tag, which is just a grammar tag loaded from paradigms.txt.
    It splits the tag into it's component parts and lines them up so we can create
    a Tag object.

    """


    #add the field 'string', which is unique and required
    kwargs = {}
    kwargs['string'] = tag

    #parse the tag and assign the tag components to the model fields
    tag = tag.split('+')
    for e in tag:
        kwargs[fieldmap[e]] = e


    #finally, add the tag to the database. whew!
    return Tag.objects.get_or_create(**kwargs)

def GT_fstResults(l):
    """
    This only works for giellatechnos fst form.
    set where to get the site in the following variables, PRETEXT is everything before
    the query word. POSTTEXT is everything after.
    Redefine this method if you are not using the website.
    """

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

def queryGenerator(l, tag):
    """
    This uses subprocess to query the generator and obtain a value for the wordform
    that is needed.
    """
    PIPE = sp.PIPE
    proc = sp.Popen(GEN_COMMAND, shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE,
                        encoding='utf-8')
    data = l + '+' + tag
    # print(data)



    kwargs = {'input':data}
    output, err = proc.communicate(**kwargs)
    return output, err

class Tagset:
    """
    paradigmFile is defined as a variable at the top of the page. It's just the
    txt file called paradigms.txt. It should contain all the possible paradigms
    for words in the language.
    It'll look like this:
    ...
    N+AN+Der/Dim+N+AN+Px1Pl+Loc
    N+AN+Der/Dim+N+AN+Px1Sg+Loc
    N+AN+Der/Dim+N+AN+Px2Pl+Loc
    ...

    This class contains paradigmDict, the keys are of the form 'N+AN' and the value
    will be a list of all the paradigms for that type of word.

    """

    def __init__(self, paradigmFile):
        paradigms = open(paradigmFile, 'r', encoding='utf8').readlines()
        #read the lines, one at a time, into a dictionary
        self.paradigmDict = {}

        for line in paradigms:
            #get the key for the dictionary enty
            components = line.split('+')

            lemmaComponents = '+'.join(components[:2])
            #should be 'N+AN'

            #now, add it to the dictionary.
            if lemmaComponents in self.paradigmDict:
                self.paradigmDict[lemmaComponents].append(line.rstrip())
            else:
                self.paradigmDict[lemmaComponents] = [line.rstrip()]



if __name__ == "__main__": main(USE_GT)
