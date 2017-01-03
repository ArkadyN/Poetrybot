from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams
from nltk.corpus import cmudict
import nltk
import pprint
from random import shuffle
import random
from nltk.corpus import stopwords
from collections import Counter
import string
import re
from Poem import Poem
import pickle
import os
import stanford
from collections import defaultdict
from datetime import datetime, date, time
from timeit import default_timer as timer
import itertools
import logging

class RoboPoet:

    patterns = [
#        [(3,'A'),(3,'A'),(3,'B')]
#        , 
#        ,[(8,'A'),(5,'B'),(7,'A'),(5,'B')]
#        ,[(8,'A'),(5,'B'),(4,'C'),(4,'C'),(5,'B')]
#        ,[(10,'A'),(6,'B'),(10,'A'),(6,'B')]
#        ,[(11,'A'), (11,'A'), (11,'B'), (11,'B')]
##        ,[(11,'A'), (11,'B'), (11,'C'), (9,'D'), (2,'B')]
#        ,[(11,'A'), (12,'A'), (5,'B'), (7,'C'),(10,'C')]
##        ,[(4,'A'),(4,'B'),(4,'C'),(4,'B'), (4,'D'),(4,'E'),(4,'D'),(4,'E')]
##        ,[(4,'A'),(4,'B'),(4,'C'),(4,'B'), (4,'D'),(4,'D'),(2,'E'),(2,'E'),(4,'D')]
#        ,[(4,'A'),(4,'B'),(4,'A'),(4,'B'), (4,'D'),(4,'E'),(4,'D'),(4,'E')]
#        ,[(4,'A'),(4,'B'),(4,'A'),(4,'B'), (4,'D'),(4,'D'),(2,'E'),(2,'E'),(4,'D')]


#        [(7,'A'), (5,'A'), (7,'B')],
        [
         (8,'A'),(8,'B'),(8,'A'),(8,'B'),(0,'NL')
        ,(8,'C'),(8,'D'),(8,'C'),(8,'D'),(0,'NL')
        ,(9,'E'),(9,'F'),(9,'E'),(9,'F'),(0,'NL')
        ,(7,'G'),(7,'G')
        ]
        ,
#         [
#          (10,'A'),(10,'B'),(10,'A'),(10,'B'),(0,'NL')
#         ,(10,'C'),(10,'D'),(10,'C'),(10,'D'),(0,'NL')
#         ,(11,'E'),(11,'F'),(11,'E'),(11,'F'),(0,'NL')
#         ,(10,'G'),(9,'G')
#         ]
                
#         ,
#         [ (9,'A'),(9,'A'),(9,'B'),(9,'B'),(8,'A')]  #Limerick
#         ,
#         [ #terza rima
#           (9,'A'),(9,'B'),(9,'A'),(0,'NL')
#         , (8,'B'),(8,'C'),(8,'B'),(0,'NL')
#         , (9,'C'),(9,'D'),(9,'C'),(0,'NL')
#          ]

#         ,[(5,'A'),(5,'B'),(5,'A'),(5,'B')]
#         ,[(6,'A'),(6,'B'),(6,'A'),(6,'B')]
#         ,[(7,'A'),(7,'B'),(7,'A'),(7,'B')]
#         ,[(8,'A'),(8,'B'),(8,'A'),(8,'B')]
#         ,[(9,'A'),(9,'B'),(9,'A'),(9,'B')]
#         ,[(10,'A'),(10,'B'),(10,'A'),(10,'B')]
#         ,[(11,'A'),(11,'B'),(11,'A'),(11,'B')]
#         ,[(12,'A'),(12,'B'),(12,'A'),(12,'B')]
#        ,[(13,'A'),(13,'B'),(13,'A'),(13,'B')]
#        ,[(14,'A'),(14,'B'),(14,'A'),(14,'B')]
#        ,[(15,'A'),(15,'B'),(15,'A'),(15,'B')]
#        ,[(16,'A'),(16,'B'),(16,'A'),(16,'B')]
#        ,[(17,'A'),(17,'B'),(17,'A'),(17,'B')]
#        ,[(18,'A'),(18,'B'),(18,'A'),(18,'B')]
#        ,[(19,'A'),(19,'B'),(19,'A'),(19,'B')]
#        ,[(20,'A'),(20,'B'),(20,'A'),(20,'B')]
#        ,[(21,'A'),(21,'B'),(21,'A'),(21,'B')]
#        ,[(22,'A'),(22,'B'),(22,'A'),(22,'B')]
#        ,[(23,'A'),(23,'B'),(23,'A'),(23,'B')]
#        ,[(24,'A'),(24,'B'),(24,'A'),(24,'B')]
#        ,[(25,'A'),(25,'B'),(25,'A'),(25,'B')]
#        ,[(26,'A'),(26,'B'),(26,'A'),(26,'B')]
#        ,[(27,'A'),(27,'B'),(27,'A'),(27,'B')]
#        ,[(28,'A'),(28,'B'),(28,'A'),(28,'B')]
#        ,[(29,'A'),(29,'B'),(29,'A'),(29,'B')]
#        ,[(30,'A'),(30,'B'),(30,'A'),(30,'B')]
    ]
    pattern_haiku = [(7,'A'), (5,'B'), (7,'C')] 
    pattern_haiku_rhymed = [(7,'A'), (5,'A'), (7,'B')] 

    def __init__(self, 
            text, 
            max_syllb_count=30, 
            max_ngram_count=10,
            min_rhyme_level=3,
            max_rhyme_level=9,
            num_retries=100
        ):
        self.max_syllb_count = max_syllb_count
        self.max_ngram_count = max_ngram_count
        self.min_rhyme_level = min_rhyme_level
        self.max_rhyme_level = max_rhyme_level
        self.num_retries = num_retries

        logging.info('RoboPoet.init() : enter')
        self.cmud = cmudict.dict()   
         
#         ngrams_fn = 'ngrams_ny.p'
#         if os.path.isfile(ngrams_fn):
#             self.ngrams = pickle.load(open(ngrams_fn,'rb'))
#         else:
        unusedgrams = 0
        usedgrams = 0
        self.ngrams =  defaultdict(set)        
        chunk_size = 50
        text_sents = sent_tokenize(text)
        for i in range(0, len(text_sents), chunk_size):
            logging.info('RoboPoet.init() : chunk {0}'.format(i))
            for gram in self.gramize(' '.join(text_sents[i:i+chunk_size])):
                sc = [self.get_syllb_count(word) for word in gram[1]]
                if self.use_gram(gram[1]) and sum(sc)<= self.max_syllb_count:
                    
                    
                    
                    #words = tuple([g for g,c in zip(gram[1],sc) if c>0]) #remove all words that could not calculate syllb count
                    #self.ngrams[sum(sc)].add((gram[0],words))
                    
                    
                    if all(a>0 for a in sc):
                        usedgrams += 1
                        words = tuple([g for g,c in zip(gram[1],sc) ])
                        self.ngrams[sum(sc)].add((gram[0],words))
                    else:
                        unusedgrams += 1
#             pickle.dump(self.ngrams, open(ngrams_fn,'wb'))
        logging.info('RoboPoet.init() : processed {0} grams'.format(
            sum([len(g[1]) for g in self.ngrams.items()])
            ))   
        logging.info('used grams {0}, unused grams {1}'.format(usedgrams, unusedgrams))
        
        #for s in self.ngrams.values():
        #    for gram in s:
        #        print( type(gram[0]), type(gram[1]) )
        #exit(0)
        
        #pprint.pprint(self.ngrams)
        #print(sum(etime)/float(len(etime)))
                    
#        pprint.pprint([(k, len(v)) for k,v in self.syllb_ngrams.items()])
#        pprint.pprint(self.syllb_ngrams[3])

#        pprint.pprint([vv  for k,v in self.syllb_ngrams.items() for vv in v if len(v) and len(vv) and vv[-1].lower() == 'in'])

    def gramize(self, sents):
        for gram in stanford.get_all_phrases(sents):
            yield gram


    def use_gram(self, gram):
        t = False
        if gram or len(gram):
            t = str.casefold(gram[-1]) not in set([
                'a', 'ain', 
                'am', 'an', 'and', 'en'
                'are', 'as', 'at', 'be', 'but', 'by', 'can', 'd', 'did', 'do', 'don', 
                'for', 'had', 'has', 'he', 'her', 'him', 'his', 'how', 'i', 'if', 'in', 'is', 'isn', 'it', 'its', 'll', 'm', 'ma', 'me', 'my', 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'or', 'our', 'out', 
                're', 's', 'she', 'so', 't', 'the', 'to', 'too', 'up', 've', 'was', 'we', 'who', 'why', 'won', 'y', 'you'
                ,'their','there'
            ])
                #'all', 
                #'any', 
                #'few', 
                #'own', 

            #s.lower() for s in stopwords.words('english') if len(s) <= 3]+['their','there','to','the']
        return t


    def get_best_poem(self, multiplier=5):
        poems = []
        for i in range(multiplier):
            poems += self.get_poems()

        logging.info('RoboPoet.get_best_poem() got {0} poems'.format(len(poems)))
        if len(poems):
            return sorted(poems, key=lambda poem: poem.score(), reverse=True)[0]
        else:
            return None

    def get_poems(self):
        poems = []
        for pat in self.patterns:
            poem = self.get_poem(pat)
            if poem:
                yield poem
    
    def get_poem(self, pattern):
        try:
            rhymes = {pat[1]:'' for pat in pattern} 
            lines = list(zip([None]*len(pattern), [None]*len(pattern))) 
            for rl in range(self.max_rhyme_level, self.min_rhyme_level, -1):
                for i in range(self.num_retries):
                    self.get_poem_first_lines(pattern, rhymes, lines, rl)
                    self.get_poem_second_lines(pattern, rhymes, lines, rl)
                    poem = Poem(lines, pattern, rl)
                    if poem.is_complete():
#                         logging.info('RoboPoet.get_poem() {0}'.format('='*30))
#                         logging.info(poem.debug_string())
                        return poem
    
            return None
        except Exception as ex:
            #todo: add exception stack printout https://docs.python.org/3.5/library/traceback.html
            logging.error('get_poem() ERROR {0}'.format(ex))
            return None

    def get_poem_first_lines(self, pattern, rhymes, lines, rhyme_level):
        for idx, pat in enumerate(pattern):
            if pat == (0,'NL'):
                lines[idx] = ('\n','\n')
            elif not rhymes[pat[1]]:
                lines[idx] = self.get_line('',pat[0],lines,False, rhyme_level)
                if lines[idx]:
                    rhymes[pat[1]] = lines[idx][1][-1]
#        print('first_lines',grams)
#        print('first_lines',rhymes)


    def get_poem_second_lines(self, pattern, rhymes, lines, rhyme_level):
        for idx, pat in enumerate(pattern):
            if rhymes[pat[1]] and not lines[idx][1]:
                lines[idx] = self.get_line(rhymes[pat[1]], pat[0], lines, True, rhyme_level) 
                if lines[idx] == (None,None):
                    rhymes[pat[1]] = ''

#        print('second_lines',lines)
#        print('second_lines',rhymes)


    def get_line(self, word, syllb_count, grams_exclude, to_rhyme, rhyme_level):
        
        r=(None,None)
        candidates = [t for t in self.ngrams[syllb_count] 
                #exclude all grams with the same last word
                if t[1][-1].lower() not in [p[1][-1].lower() for p in grams_exclude if p and p[1] and len(p[1])]
                #and nltk.distance.edit_distance(word.lower(), t[1][-1].lower()) > 2 
                ]
        
        if len(candidates):
            if to_rhyme and len(word):
                candidates_rhymed = [cand for cand in candidates 
                    if self.does_rhyme(word,cand[1][-1], rhyme_level)
                    ]
                if len(candidates_rhymed):
                    r = random.choice(candidates_rhymed)
            else:
                r = random.choice(candidates)
        return r        
        


#     def does_rhyme(self, word1, word2, rhyme_level):
#         #removed this to get better rhymes
# #        if word1.lower()[-3:] == 'ing' and word2.lower()[-3:] == 'ing':
# #            return True
# 
#         w1s = self.cmud.get(word1.lower(), [])
#         w2s = self.cmud.get(word2.lower(), [])
#         #there can be multiple pronunciations.  need to compare all with all
#         for word1s, word2s in itertools.product(w1s,w2s):
#             c=0
#             for a,b in zip(reversed(word1s), reversed(word2s)):
#                 if a==b:
#                     c+=1
#                 else:
#                     return c>=rhyme_level
# 
#         return c>=rhyme_level


    #http://stackoverflow.com/a/25714769
    def does_rhyme(self, word1, word2, rhyme_level):
            #sorted(list(set([p for ppp in list(cmudict.dict().values()) for pp in ppp for p in pp])))
            #['AA0', 'AA1', 'AA2', 'AE0', 'AE1', 'AE2', 'AH0', 'AH1', 'AH2', 'AO0', 'AO1', 'AO2', 'AW0', 'AW1', 'AW2', 'AY0', 'AY1', 'AY2', 'B', 'CH', 'D', 'DH', 'EH0', 'EH1', 'EH2', 'ER0', 'ER1', 'ER2', 'EY0', 'EY1', 'EY2', 'F', 'G', 'HH', 'IH0', 'IH1', 'IH2', 'IY0', 'IY1', 'IY2', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW0', 'OW1', 'OW2', 'OY0', 'OY1', 'OY2', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH0', 'UH1', 'UH2', 'UW', 'UW0', 'UW1', 'UW2', 'V', 'W', 'Y', 'Z', 'ZH']


        if str.casefold(word1) == str.casefold(word2)[-len(str.casefold(word1)):] or str.casefold(word2) == str.casefold(word1)[-len(str.casefold(word2)):] :
            #logging.info('does_rhyme() [{0}] [{1}] contain each other.  returning false.'.format(word1, word2))
            return False
        
        w1s = self.cmud.get(str.casefold(word1), [])
        w2s = self.cmud.get(str.casefold(word2), [])
        #there can be multiple pronunciations.  need to compare all with all
        for word1s, word2s in itertools.product(w1s,w2s):
            if self._does_rhyme_internal(word1s, word2s, rhyme_level):
                return True
            
        return False
            
    #last rhyming vowel is more important than last rhyming consonant
    def _does_rhyme_internal(self, word1s, word2s, rhyme_level):
        last_rhyming_vowel_idx = -1
        for idx,(a,b) in enumerate(zip(reversed(word1s), reversed(word2s))):
            if a==b:
                if a[-1].isdigit() and a[:-1] == b[:-1]:
                    last_rhyming_vowel_idx = idx
            else:
                break
        
        return last_rhyming_vowel_idx+1 >= rhyme_level
        
        



    #http://stackoverflow.com/a/4103234
    def get_syllb_count(self, word):
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmud[word.lower()]][0]
        except:
            return 0


if __name__ == '__main__':
    logFormatter = logging.Formatter("%(asctime)s : %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
#     fileHandler = logging.handlers.TimedRotatingFileHandler('RoboPoet3.log', when='D', interval=1, backupCount=1000)
#     fileHandler.setFormatter(logFormatter)
#     logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)    
   

    p = RoboPoet('Return a string containing a printable representation of an object. For many types, this function makes an attempt to return a string. Here"s an example, where the objects are lists.')
#    for i in range(1,6):
##        print(p.get_line('wing',i,1,['a'],True,2))
#        print(p.get_line('sample',i,1,['a'],True,2))
#     for i in range(1):
# #        print(p.get_poem(RoboPoet.patterns[0], rhyme_level=4))
#         for poem in p.get_poems():
#             logging.info('-'*10)
#             logging.info(poem)

    print(p.does_rhyme('action','inaction',5))
    print(p.does_rhyme('separation','corporation',5))
    print(p.does_rhyme('separation','corporation',6))
    print(p.does_rhyme('circumstances','audiences',5))

