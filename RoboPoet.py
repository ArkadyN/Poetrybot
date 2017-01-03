from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams
from nltk.corpus import cmudict
import nltk
import pprint
from random import shuffle
from nltk.corpus import stopwords
from collections import Counter
import string
import re
from Poem2 import Poem
import pickle
import os
from collections import defaultdict
import itertools
import random
from datetime import datetime
from nltk.corpus import words


class RoboPoet:

    patterns = [
#            [(('NN',),1,''), (('VBG',),3,'ING'), (('EOL',),1,'')],
#            [(('VBG','VBG'),4,'ING'), (('EOL',),1,'')],

            [
            (('RB','VBG'),6,'ING'),(('EOL',),1,''),
            (('RB','VBG'),5,'ING'),(('EOL',),1,''),
            (('RB','NN'),6,'ING'),(('EOL',),1,''),
            (('RB','VBG'),6,'ING'),(('EOL',),1,''),
            (('RB','JJ'),6,'ING'),(('EOL',),1,''),
            (('RB','NN'),6,'ING'),(('EOL',),1,''),
            (('NNP','CC','JJ'),6,'A'), (('EOL',),1,''),
            (('JJ','CC','JJ'),6,'A'), (('EOL',),1,''),
            (('EOL',),1,'')
            ],[
            (('VBG',),4,'ING'), (('EOL',),1,''),
            (('VBG',),4,'ING'), (('EOL',),1,''),
            (('VBG','JJ'),6,'B'),(('EOL',),1,''),
            #(('JJ',),4,'ING'), (('EOL',),1,''),
            (('VBG',),4,'ING'), (('EOL',),1,''),
            (('VBN',),4,'B'), (('EOL',),1,''),
            (('VBG',),4,'ING'), (('EOL',),1,''),
            (('EOL',),1,''),
            (('VBN',),5,'A')
            ]
                ,
            [
            ( ('NNP', 'VBD', 'IN', 'DT', 'NN', 'DT', 'NN') , 10, 'A' ), (('EOL',),1,''),
            ( ('NNP', 'VBD', 'DT', 'NN', 'CC', 'CD') , 10, 'B' ), (('EOL',),1,''),
            ( ('NNP', 'VBD', 'DT', 'JJS', 'IN', 'DT', 'PRP$', 'NN') , 10, 'A' ), (('EOL',),1,''),
            ( ('CC', 'PDT', 'DT', 'JJS', 'PRP$', 'JJ') , 10, 'B' ), (('EOL',),1,''),
            ]
                ,
                
            [
            ( ('RB', 'JJ') , 4 ,'A' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 4 ,'B' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 4 ,'C' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 4 ,'B' ), (('EOL',),1,'')
            ],[
            ( ('RB', 'JJ') , 4 ,'E' ), (('EOL',),1,''),
            ( ('RB', 'VBG') , 4 ,'F' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 4 ,'G' ), (('EOL',),1,''),
            ( ('RB', 'VBG') , 4 ,'F' ), (('EOL',),1,''),
            ]
                                ,
                
            [
            ( ('RB', 'JJ') , 5 ,'A' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 5 ,'B' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 5 ,'C' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 5 ,'B' ), (('EOL',),1,'')
            ],[
            ( ('RB', 'JJ') , 5 ,'E' ), (('EOL',),1,''),
            ( ('RB', 'VBG') , 5 ,'F' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 5 ,'G' ), (('EOL',),1,''),
            ( ('RB', 'VBG') , 5 ,'F' ), (('EOL',),1,''),
            ]
                ,
                
            [
            ( ('RB', 'JJ') , 6 ,'A' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 6 ,'B' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 6 ,'C' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 6 ,'B' ), (('EOL',),1,'')
            ],[
            ( ('RB', 'JJ') , 6 ,'E' ), (('EOL',),1,''),
            ( ('RB', 'VBG') ,6 ,'F' ), (('EOL',),1,''),
            ( ('RB', 'JJ') , 6 ,'G' ), (('EOL',),1,''),
            ( ('RB', 'VBG') ,6 ,'F' ), (('EOL',),1,''),
            ]

                ,
            [
            ( ('PRP', 'VBD', 'DT', 'NN', 'CC', 'VBD', 'PRP', 'TO', 'VB') , 11 ,'A' ), (('EOL',),1,''),
            ( ('PRP', 'VBD', 'DT', 'NN', 'CC', 'VB', 'IN', 'DT', 'NN') , 11 ,'A' ), (('EOL',),1,''),
            ( ('PRP$', 'IN', 'PRP', 'VBD', 'CC', 'PRP$', 'NN', 'PRP', 'PRP$', 'NN') , 11 ,'B' ), (('EOL',),1,''),
            ( ('PRP', 'VBD', 'IN', 'NN', 'IN', 'TO', 'VB', 'TO', 'VB') , 9 ,'B' ), (('EOL',),1,''),
            ]
                
                
                
                
                
#

#            [
#            ('RB',2,''), ('VBG',2,'ING'), ('EOL',1,''),
#            ('RB',2,''), ('VBG',2,'ING'), ('EOL',1,''),
#            ('RB',2,''), ('NN',2,'ING'), ('EOL',1,''),
#            ('RB',2,''), ('VBG',2,'ING'), ('EOL',1,''),
#            ('RB',2,''), ('JJ',2,'D'), ('EOL',1,''),
#            ('RB',2,''), ('NN',2,'E'), ('EOL',1,''),
#            ('NNP',2,''),('CC',1,''), ('JJ',2,'D'), ('EOL',1,''),
#            ('JJ',2,''),('CC',1,''), ('JJ',2,'E'), ('EOL',1,''),
#            ('EOL',1,''),
##            ('VBG',2,'ING'), ('VBG',2,'ING'), ('EOL',1,''),
##            ('NNP',1,''),('CC',1,''), ('NN',2,'ING'), ('EOL',1,''),
##            ('IN',1,''),('CC',1,''), ('JJ',2,'F'), ('EOL',1,''),
##            ('NNS',2,''), ('VBG',2,'ING'), ('EOL',1,''),
##            ('NNP',2,''), ('NN',2,'ING'), ('EOL',1,''),
##            ('RB',2,''), ('VBG',2,'ING'), ('EOL',1,''),
##            ('JJ',2,''), ('NN',2,'G'), ('EOL',1,''),
##            ('VBG',4,'ING'), ('EOL',1,''),
##            ('EOL',1,''),
#            ('VBG',4,'ING'), ('EOL',1,''),
#            ('VBG',4,'ING'), ('EOL',1,''),
#            ('VBG',2,'ING'), ('JJ',2,'H'), ('EOL',1,''),
#            ('JJ',4,'ING'), ('EOL',1,''),
#            ('VBG',4,'ING'), ('EOL',1,''),
#            ('VBN',4,'I'), ('EOL',1,''),
#            ('VBG',4,'ING'), ('EOL',1,''),
#            ('EOL',1,''),
#            ('VBN',4,'I')
#            ]
    ]

    def __init__(self, 
            text, 
            max_syllb_count=50, 
            max_ngram_count=30, 
            max_ngram_2_count=3,
            min_rhyme_level=0,
            max_rhyme_level=9,
            num_retries=3
        ):
        print(datetime.now(), 'Init start')
        self.max_syllb_count = max_syllb_count
        self.max_ngram_count = max_ngram_count
        self.max_ngram_2_count = max_ngram_2_count
        self.min_rhyme_level = min_rhyme_level
        self.max_rhyme_level = max_rhyme_level
        self.num_retries = num_retries

        cmud_rhymes_fn = 'cmud_rhymes.p'
        self.cmud = cmudict.dict()
        self.cmue = cmudict.entries()
        if os.path.isfile(cmud_rhymes_fn):
            self.cmud_rhymes = pickle.load(open(cmud_rhymes_fn,'rb'))
        else:
            self.cmud_rhymes = {
                r:[(word,v) for word,v in cmudict.dict().items() if v[0][-1] == r] 
                for r in set([v[0][-1] for k,v in cmudict.dict().items()])
            }
            pickle.dump(self.cmud_rhymes, open(cmud_rhymes_fn,'wb'))
        print(datetime.now(), 'Loaded rhymes')

        self.ngrams_2 =  defaultdict(set)
        secondary_grams_fn = 'secondary_grams_words.p'
        if os.path.isfile(secondary_grams_fn):
            self.ngrams_2 = pickle.load(open(secondary_grams_fn, 'rb'))
        else:
            for idx, word in enumerate(words.words()):
                sc = self.get_syllb_count(word)
                if sc>0:
                    self.ngrams_2[sc].add((tuple([word]),tuple([pos[1] for pos in nltk.pos_tag([word])])) )
            pickle.dump(self.ngrams_2, open(secondary_grams_fn, 'wb'))
        print(datetime.now(), 'processed second grams', len(self.ngrams_2))

        
#        self.ngrams_2 =  defaultdict(set)
#        secondary_grams_fn = 'secondary_grams_kjb.p'
#        if os.path.isfile(secondary_grams_fn):
#            self.ngrams_2 = pickle.load(open(secondary_grams_fn, 'rb'))
#        else:
#            for idx, sent in enumerate(nltk.corpus.gutenberg.sents('bible-kjv.txt')):
#                sent = ' '.join(sent)
#                for gram in self.gramize(sent, self.max_ngram_2_count):
#                    sc = [self.get_syllb_count(word) for word in gram]
#                    gram = [g for g,c in zip(gram,sc) if c>0] #remove all words that could not calculate syllb count
#                    self.ngrams_2[sum(sc)].add((tuple(gram),tuple([pos[1] for pos in nltk.pos_tag(gram)])) )
#            pickle.dump(self.ngrams_2, open(secondary_grams_fn, 'wb'))
#        print(datetime.now(), 'processed second grams')
        

        #http://stackoverflow.com/a/32336935
        self.ngrams =  defaultdict(set)
        for idx, sent in enumerate(sent_tokenize(text)):
            for gram in self.gramize(sent, self.max_ngram_count):
                sc = [self.get_syllb_count(word) for word in gram]
                gram = [g for g,c in zip(gram,sc) if c>0] #remove all words that could not calculate syllb count
                self.ngrams[sum(sc)].add((tuple(gram),tuple([pos[1] for pos in nltk.pos_tag(gram)])) )
        print(datetime.now(), 'processed grams', len(self.ngrams))        
        
        
#        pprint.pprint(self.ngrams)                    
#        exit(0)
#        pprint.pprint([(k, len(v)) for k,v in self.syllb_ngrams.items()])
#        pprint.pprint(self.syllb_ngrams[3])

#        pprint.pprint([vv  for k,v in self.syllb_ngrams.items() for vv in v if len(v) and len(vv) and vv[-1].lower() == 'in'])



    def gramize(self, sent, max_ngram_count):
        for i in range(1,max_ngram_count+1):
            for gram in self.ngramize_all_grams(self.tokenize(sent), i):
                yield gram

    def ngramize_all_grams(self, tokens, i):
        #all ngrams
        return ngrams(tokens, i)
        
    def ngramize_sent_starts(self, tokens, i):
        #all grams starting with a sentence
        if tokens and len(tokens)>=i:
            return [tokens[:i]]
        else:
            return ('')

    def ngramize_picky_start(self, tokens, i):
        #all grams starting with a noun
        for gram in ngrams(tokens, i):
            if nltk.pos_tag(gram)[0][1] in [
                    #http://stackoverflow.com/a/38264311
                    ''
                    #,'CC'    #Coordinating conjunction
                    #,'CD'    #Cardinal number
                    #,'DT'    #Determiner
                    #,'EX'    #Existential there
                    #,'FW'    #Foreign word
                    ,'IN'    #Preposition or subordinating conjunction
                    ,'JJ'    #Adjective
                    ,'JJR'    #Adjective, comparative
                    ,'JJS'    #Adjective, superlative
                    #,'LS'    #List item marker
                    #,'MD'    #Modal
                    ,'NN'    #Noun, singular or mass
                    ,'NNS'    #Noun, plural
                    ,'NNP'    #Proper noun, singular
                    ,'NNPS'    #Proper noun, plural
                    ,'PDT'    #Predeterminer
                    #,'POS'    #Possessive ending
                    ,'PRP'    #Personal pronoun
                    ,'PRP$'    #Possessive pronoun
                    ,'RB'    #Adverb
                    ,'RBR'    #Adverb, comparative
                    ,'RBS'    #Adverb, superlative
                    ,'RP'    #Particle
                    #,'SYM'    #Symbol
                    #,'TO'    #to
                    ,'UH'    #Interjection
                    ,'VB'    #Verb, base form
                    #,'VBD'    #Verb, past tense
                    ,'VBG'    #Verb, gerund or present participle
                    #,'VBN'    #Verb, past participle
                    ,'VBP'    #Verb, non-3rd person singular present
                    ,'VBZ'    #Verb, 3rd person singular present
                    #,'WDT'    #Wh-determiner
                    #,'WP'    #Wh-pronoun
                    #,'WP$'    #Possessive wh-pronoun
                    #,'WRB'    #Wh-adverb
                    ]:
                yield gram


    def ngramize(self, tokens, i):
        #return self.ngramize_all_grams(tokens, i)
        #return self.ngramize_sent_starts(tokens, i)
        return self.ngramize_picky_start(tokens, i)
        

    def tokenize(self, sent):
        sent = sent.replace('\n',' ')
        sent = sent.replace('\r',' ')
        sent = re.sub('['+ re.escape(string.punctuation) + ']', '', sent)
        return word_tokenize(sent)


    def get_poems(self):
        poems = []
        for pat in self.patterns: 
            poem = self.get_poem(pat)
            if poem:
                yield poem

    def get_poem(self, pattern):
#            [(['NN'],2,''), (['NNS'],1,'ING'), (['EOL'],1,'')],
#            [(['NN','NNS'],2,'ING'), (['EOL'],1,'')],
        print('get_poem()','-'*20)
        rhymes = {pat[2]:'' for pat in pattern} # if pat[2] != ''}
        rhymes['ING']='ing'
        grams = [''] * len(pattern)
#        for rl in range(self.max_rhyme_level, self.min_rhyme_level, -1):
#            print(pattern)
#            print(rhymes)
#            print(rl, grams)
        rl = 1    
        for i in range(self.num_retries):
            self.get_poem_first_lines(pattern, rhymes, grams, rl)
            self.get_poem_second_lines(pattern, rhymes, grams, rl)
            poem = Poem(grams, pattern, rl)
            if poem.is_complete():
                return poem

        return None


    def get_poem_first_lines(self, pattern, rhymes, grams, rhyme_level):
        for idx, pat in enumerate(pattern):
            if pat[0][0]=='EOL':
                grams[idx]=['\n']
                rhymes[idx]='EOL'
            elif pat[2] == '':
                grams[idx] = self.get_gram(pat[0], pat[1],'',rhyme_level, grams)
#            elif pat[2] == 'ING' and grams[idx] == '':
#                grams[idx] = self.get_gram(pat[0], pat[1],'ING',rhyme_level)
#                if grams[idx]:
#                    rhymes[pat[2]] = grams[idx][-1]
            elif not rhymes[pat[2]]:
                grams[idx] = self.get_gram(pat[0], pat[1],rhymes[pat[2]],rhyme_level, grams)
                if grams[idx]:
                    rhymes[pat[2]] = grams[idx][-1]
#        print('first_lines',grams)
#        print('first_lines',rhymes)


    def get_poem_second_lines(self, pattern, rhymes, grams, rhyme_level):
        for idx, pat in enumerate(pattern):
            if rhymes[pat[2]] and (grams[idx] == [] or grams[idx]==''):
                grams[idx] = self.get_gram(pat[0], pat[1],rhymes[pat[2]],rhyme_level, grams)
#                print('get_poem_second_lines', grams[idx], bool(grams[idx]))
                if grams[idx]:
                    rhymes[pat[2]] = grams[idx][-1]
                else:
                    rhymes[pat[2]] = []

#        print('second_lines',grams)
#        print('second_lines',rhymes)


    def get_gram(self, pos, syllb_count, word, rhyme_level, grams):
#        print('get_gram----------', pos, syllb_count, word, rhyme_level)
        gram = self.get_gram_whole(pos, syllb_count, word, rhyme_level, self.ngrams)
#        print('get_gram','gram_while returned', gram)
        if gram == ():
#            print('get_gram','calling gram_broken')
            gram = self.get_gram_broken(pos, syllb_count, word, rhyme_level, self.ngrams)
            
        if gram in grams:
             print('duplicate found!!!')
             gram = ()   
            
#        if gram == ():
#            #lets try to go to a secondary source
##            print('get_gram from second----------', pos, syllb_count, word, rhyme_level)
#            gram = self.get_gram_whole(pos, syllb_count, word, rhyme_level, self.ngrams_2)
##            print('get_gram from second','gram_while returned', gram)
#            if gram == ():
##                print('get_gram from second','calling gram_broken')
#                gram = self.get_gram_broken(pos, syllb_count, word, rhyme_level, self.ngrams_2)                
            
        return gram

    def get_gram_broken(self, pos, syllb_count, word, rhyme_level, source):
        #lets break up and see if we can get it in pieces
        combos = [c for c in self.multichoose(len(pos),syllb_count) if all(c)]
        shuffle(combos)
#        print('get_gram_broken', pos, syllb_count, word, rhyme_level, combos)
        if not combos:
            return ()
        for combo in combos:
#            print('get_gram_broken', combo)
            r = []
            for idx,c in enumerate(combo[:-1]):
                v = self.get_gram_whole((pos[idx],),c,'',rhyme_level, source)
#                print('get_gram_broken','called gramwhole',v, bool(v))
                if v:
                    r += v
                else:
                    r = ()
                    break
            else: #last word needs to rhyme
#            print('get_gram_broken','calling gramwhole last',pos[-1],combo[-1])
                v = self.get_gram_whole((pos[-1],),combo[-1],word,rhyme_level, source)
#                print('get_gram_broken','last called gramwhole',v, bool(v))
                if v:
                    r += v
                else:
                    r = ()
                    
            if len(r):
                break

#        print('get_gram_broken','returning',r)
        return tuple(r)

        
    def get_gram_whole(self, pos, syllb_count, word, rhyme_level, source):
#        print('get_word_whole enter',pos,syllb_count, word, rhyme_level)
        r=()
        candidates = [gram[0] for gram in source[syllb_count] if gram[1] == pos]
        #print(candidates)
        if len(candidates):
            if len(word):
                for rl in range(self.max_rhyme_level, self.min_rhyme_level, -1):
                    candidates_rhymed = [cand for cand in candidates 
                        if self.does_rhyme(word,cand[-1],rl)] #rhyme_level)]
#                print(word, candidates_rhymed)
                    if len(candidates_rhymed):
                        r = random.choice(candidates_rhymed)
                        break
#                    else:
#                        print('zero candidates rhymed', pos, syllb_count, word, len(source))
            else:
                r = random.choice(candidates)

#        else:
#            print('zero candidates', pos, syllb_count, word, len(source))
#        print('get_word_whole returning',r)
        return r

    def does_rhyme(self, word1, word2, rhyme_level):
        if word1.lower()[-3:] == 'ing' and word2.lower()[-3:] == 'ing':
            return True

        w1s = self.cmud.get(word1.lower(), [])
        w2s = self.cmud.get(word2.lower(), [])
        #there can be multiple pronunciations.  need to compare all with all
        for word1s, word2s in itertools.product(w1s,w2s):
            c=0
            for a,b in zip(reversed(word1s), reversed(word2s)):
                if a==b:
                    c+=1
                else:
                    return c>=rhyme_level

        return c>=rhyme_level


    #http://mathoverflow.net/a/9494
    def multichoose(self,n,k):
        if k < 0 or n < 0: return "Error"
        if not k: return [[0]*n]
        if not n: return []
        if n == 1: return [[k]]
        return [[0]+val for val in self.multichoose(n-1,k)] + \
            [[val[0]+1]+val[1:] for val in self.multichoose(n,k-1)]

    #http://stackoverflow.com/a/4103234
    def get_syllb_count(self, word):
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmud[word.lower()]][0]
        except:
            return 0


if __name__ == '__main__':

    p = RoboPoet('Return a string containing a printable representation of an object. For many types, this function makes an attempt to return a string. Here"s an example, where the objects are lists.')
#    for i in range(1,6):
##        print(p.get_line('wing',i,1,['a'],True,2))
#        print(p.get_line('sample',i,1,['a'],True,2))
    for i in range(1):
        print(p.get_poem(RoboPoet.patterns[0]))
#        print(p.get_poem(RoboPoet.patterns[1]))
#        for poem in p.get_poems():
#            print('-'*10)
#            print(poem)



