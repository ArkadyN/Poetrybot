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
from Poem import Poem
import pickle
import os


class RoboPoet:

    patterns = [
#        [(3,'A'),(3,'A'),(3,'B')]
#        ,
        [(7,'A'), (5,'A'), (7,'B')] 
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

        ,[(5,'A'),(5,'B'),(5,'A'),(5,'B')]
        ,[(6,'A'),(6,'B'),(6,'A'),(6,'B')]
        ,[(7,'A'),(7,'B'),(7,'A'),(7,'B')]
        ,[(8,'A'),(8,'B'),(8,'A'),(8,'B')]
        ,[(9,'A'),(9,'B'),(9,'A'),(9,'B')]
        ,[(10,'A'),(10,'B'),(10,'A'),(10,'B')]
        ,[(11,'A'),(11,'B'),(11,'A'),(11,'B')]
        ,[(12,'A'),(12,'B'),(12,'A'),(12,'B')]
        ,[(13,'A'),(13,'B'),(13,'A'),(13,'B')]
        ,[(14,'A'),(14,'B'),(14,'A'),(14,'B')]
        ,[(15,'A'),(15,'B'),(15,'A'),(15,'B')]
        ,[(16,'A'),(16,'B'),(16,'A'),(16,'B')]
        ,[(17,'A'),(17,'B'),(17,'A'),(17,'B')]
        ,[(18,'A'),(18,'B'),(18,'A'),(18,'B')]
        ,[(19,'A'),(19,'B'),(19,'A'),(19,'B')]
        ,[(20,'A'),(20,'B'),(20,'A'),(20,'B')]
        ,[(21,'A'),(21,'B'),(21,'A'),(21,'B')]
        ,[(22,'A'),(22,'B'),(22,'A'),(22,'B')]
        ,[(23,'A'),(23,'B'),(23,'A'),(23,'B')]
        ,[(24,'A'),(24,'B'),(24,'A'),(24,'B')]
        ,[(25,'A'),(25,'B'),(25,'A'),(25,'B')]
        ,[(26,'A'),(26,'B'),(26,'A'),(26,'B')]
        ,[(27,'A'),(27,'B'),(27,'A'),(27,'B')]
        ,[(28,'A'),(28,'B'),(28,'A'),(28,'B')]
        ,[(29,'A'),(29,'B'),(29,'A'),(29,'B')]
        ,[(30,'A'),(30,'B'),(30,'A'),(30,'B')]
    ]
    pattern_haiku = [(7,'A'), (5,'B'), (7,'C')] 
    pattern_haiku_rhymed = [(7,'A'), (5,'A'), (7,'B')] 

    def __init__(self, 
            text, 
            max_syllb_count=50, 
            max_ngram_count=10, 
            min_rhyme_level=2,
            max_rhyme_level=9,
            num_retries=100
        ):
        self.max_syllb_count = max_syllb_count
        self.max_ngram_count = max_ngram_count
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

        self.syllb_ngrams = {i:[] for i in range(0,self.max_syllb_count+1)}

        for idx, sent in enumerate(sent_tokenize(text)):
            for i in range(1,self.max_ngram_count+1):
                for gram in self.ngramize(self.tokenize(sent), i):
                    sc = [self.get_syllb_count(word) for word in gram]
                    gram = [g for g,c in zip(gram,sc) if c>0] #remove all words that could not calculate syllb count
                    if self.use_gram(gram):
                        self.syllb_ngrams[sum(sc)].append(gram)

#        pprint.pprint(self.syllb_ngrams)                    
#        pprint.pprint([(k, len(v)) for k,v in self.syllb_ngrams.items()])
#        pprint.pprint(self.syllb_ngrams[3])

#        pprint.pprint([vv  for k,v in self.syllb_ngrams.items() for vv in v if len(v) and len(vv) and vv[-1].lower() == 'in'])


    def use_gram(self, gram):
        t = False
        if gram or len(gram):
            t = str.casefold(gram[-1]) not in set([
                'a', 'ain', 
                'am', 'an', 'and', 
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





    def get_line(self,word, syllb_count, sent_num, grams_exclude, to_rhyme, rhyme_level):
        #if to_rhyme: print('get_line()',word)
        r = None
        ngrams = [
                t for t in self.syllb_ngrams[syllb_count] 
#                if t not in grams_exclude

#                if [a.lower() for a in t[1]] not in 
#                [[g.lower() for g in gram] for gram in grams_exclude]

                #exclude all grams with the same last word
                if t[-1].lower() not in [p[-1].lower() for p in grams_exclude if p and len(p)]
                ]
        #if to_rhyme: print('get_line()',ngrams)

        if not ngrams and not len(ngrams):
            return None

        shuffle(ngrams) #randomize
        if not word and not to_rhyme:
            r = ngrams[0]
        else:
            lor = self.list_of_rhymes(word, rhyme_level)
#            if to_rhyme: print('get_line()',lor)
            for gram in ngrams:
                if to_rhyme:
                    if word.lower() != gram[-1].lower() and gram[-1].lower() in lor:
                        r = gram
                        break
                else:
                    if gram[-1].lower() not in lor:
                        r = gram
                        break

#        if to_rhyme and r:
#            print(word, to_rhyme, 'returning',r)
#        pprint.pprint(ngrams)                    
        return r

    def get_poems(self):
        poems = []
        for pat in self.patterns: # *2:
#            for rl in range(self.max_rhyme_level, self.min_rhyme_level, -1):
#                print(rl)
#                poem = self.get_poem(pat, rl)
#                #print (rl, poem.is_complete(), '\n', poem)
#                if poem.is_complete():
#                    poems.append(poem)
#                    break

            poem = self.get_poem(pat)
            if poem:
                yield poem
        #        poems.append(poem)

        #return poems


    def get_poem(self, pattern):
        for rl in range(self.max_rhyme_level, self.min_rhyme_level, -1):
#            print(rl)
            rhymes = {pat[1]:'' for pat in pattern}
            lines = [['']] * len(pattern)
            self.get_poem_2(pattern, rhymes, lines, rl)
            poem = Poem(lines, pattern, rl)
            if poem.is_complete():
                return poem
        return None


    def get_poem_2(self, pattern, rhymes, lines, rhyme_level):
        for i in range(self.num_retries):        
#            if not i%20:
#                print('num_retries',i)
            self.get_poem_first_lines(pattern, rhymes, lines, rhyme_level)
            self.get_poem_second_lines(pattern, rhymes, lines, rhyme_level)
#            print(i,lines,rhymes,
#            len([line for line in lines if not line or line == [] or line == ['']])
#            )
#            if not len([line for line in lines if not line]):
            if len([line for line in lines if not line or line == [] or line == ['']]) == 0:
#                print('breaking',lines)
                break

        #return lines

    def get_poem_first_lines(self, pattern, rhymes, lines, rhyme_level):
        for idx, pat in enumerate(pattern):
            if not rhymes[pat[1]]:
                lines[idx] = self.get_line('',pat[0],0,lines,False, rhyme_level)
                if lines[idx]:
                    rhymes[pat[1]] = lines[idx][-1]
#        print('first_lines',lines)
#        print('first_lines',rhymes)

    def get_poem_second_lines(self, pattern, rhymes, lines, rhyme_level):
        for idx, pat in enumerate(pattern):
            if rhymes[pat[1]] and (not lines[idx] or lines[idx]==[] or lines[idx]==['']):
                lines[idx] = self.get_line(rhymes[pat[1]], pat[0], 0, lines, True, rhyme_level) 
                if not lines[idx]:
                    rhymes[pat[1]] = ''

#        print('second_lines',lines)
#        print('second_lines',rhymes)

    def list_of_rhymes(self, inp, level):
        syllables = self.cmud.get(inp.lower(),[])
        rhymes = []
        for syllable in syllables:
            try:
                rhymes += [
                    word.lower() for word, prons in self.cmud_rhymes[syllable[-1]]
                    for pron in prons if pron[-level:] == syllable[-level:]
                    ]
            except Exception as e:
                print('list_of_rhymes error', inp, level, e)
                pass

        return set(rhymes)

    #http://stackoverflow.com/a/25714769
#    def list_of_rhymes(self, inp, level):
#        entries = self.cmue
#        syllables = [(word, syl) for word, syl in entries if word == inp.lower()]
#        rhymes = []
#        for (word, syllable) in syllables:
#            rhymes += [word.lower() for word, pron in entries if pron[-level:] == syllable[-level:]]
#        return set(rhymes)

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
#        print(p.get_poem(RoboPoet.patterns[0], rhyme_level=4))
        for poem in p.get_poems():
            print('-'*10)
            print(poem)



