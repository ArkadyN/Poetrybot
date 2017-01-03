#http://stackoverflow.com/questions/34968716/why-stanford-parser-with-nltk-is-not-correctly-parsing-a-sentence
from nltk.tag.stanford import StanfordNERTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from datetime import datetime
import logging



ner_tagger = StanfordNERTagger(
    model_filename='/usr/share/stanford/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz'
    ,path_to_jar='/usr/share/stanford/stanford-ner-2015-12-09/stanford-ner.jar'
    )
        
parser = StanfordParser(
    model_path="/usr/share/stanford/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"
    ,path_to_models_jar='/usr/share/stanford/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
    ,path_to_jar='/usr/share/stanford/stanford-parser-full-2015-12-09/stanford-parser.jar'
    #,encoding='utf8'
    #,verbose=True
    )
        
dep_parser = StanfordDependencyParser(
    model_path="/usr/share/stanford/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"
    ,path_to_models_jar='/usr/share/stanford/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
    ,path_to_jar='/usr/share/stanford/stanford-parser-full-2015-12-09/stanford-parser.jar'
    #,encoding='utf8'
    #,verbose=True
    )
        
        
# def find_nps(tree):
#     nps = []
#     for subtree in tree:
#         if type(subtree) == nltk.tree.Tree:
#             if subtree.label() == 'NP':
#                 nps.append(' '.join(subtree.leaves()))
#             else:
#                 #print('into',type(subtree), subtree.label(),subtree)
#                 nps += find_nps(subtree)
# 
#     return nps

#https://gist.github.com/nlothian/9240750
ignore = set(['ROOT','S','.','FRAG','WRB','WP','WHPP','WHNP','WHADVP',
                      'WDT','TO','RP','RPT','PRP$','PRP',
                      'WP$','X'
                      ,'SP','DT'
                      ])

def get_all_phrases(sents, ignore_phrases = ignore):
    sents = sents.encode('utf-8','ignore').decode('ascii', 'ignore')
    all = sent_tokenize(sents)   
    trees = parser.raw_parse_sents(all)   
    for tree in trees:
        for t in tree:
            if type(t) == nltk.tree.Tree and t.label() == 'ROOT':
                for p in get_all_phrases_inner(t, ignore_phrases):
                    yield p
                


def get_all_phrases_inner(tree, ignore_phrases):
    p = []
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            if subtree.label() not in ignore_phrases:
                #print('subtree into',type(subtree), subtree.label(),subtree.leaves())
                p.append( (subtree.label(), subtree.leaves()) )

            p += get_all_phrases_inner(subtree, ignore_phrases)
    return p





def get_stats(sent):
    try:
        parsed_Sentence = parser.raw_parse(sent)
#        for line in parsed_Sentence:
#            return(line.height(), len(line.productions()))

        line = list(parsed_Sentence)[0]
        return(line.height(), len(line.productions()))

    except Exception as e:
        logging.error('stanford.get_stats() ERROR : {0} {1}'.format(sent,e))
        return(0,0)



if __name__ == '__main__':
    
    logFormatter = logging.Formatter("%(asctime)s : %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
#     fileHandler = logging.handlers.TimedRotatingFileHandler('stanford.log', when='D', interval=1, backupCount=1000)
#     fileHandler.setFormatter(logFormatter)
#     logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)        
    
    
    sentences = [
                #'My name is Joe Boxer and I like IBM',
               'i hate chicken.  that is what i said.'
                #,'i hate linear algebra'
                #,'i fuckin hate chicken'
                #,'i fuckin hate linear algebra'
                #,'i fucking hate linear algebra'
                #,'I hate it when people say the Ottomans were tolerant.'


                #,'cats of the Felis genus could purr'
                #,'killed without endangering the cat'
                #,'that substance at less than one part per'
                #,'The English word cat Old English catt'

                #,'cats of the Felis genus could purr \n killed without endangering the cat \n that substance at less than one part per \n The English word cat Old English catt'


#  and to months males although this can vary
#  that falling cats often land on their feet
#  Cats are capable of walking very
#  and the tail is little used for this feat
#
#   this line of partially domesticated
#   aspects have increased vulnerability
#   introduced cats can be more complicated
#   account for the cats spinal mobility






                ]
        
    
    for sent in sentences:
        print('-'*10)
        print(sent)


        print(get_stats(sent))
        print(list(get_all_phrases(sent)))
        continue



    #    print(ner_tagger.tag(nltk.word_tokenize(sent)))
        parsed_Sentence = parser.raw_parse(sent)
    
    
    #    print(find_nps(parsed_Sentence))
        print(type(parsed_Sentence))
    #    print(parsed_Sentence)
        for line in parsed_Sentence:
            print(type(line))
    #        print(dir(line))
    #        print(vars(line))
            print(line.label())
            print('===',line)
            print(line.height(), line.productions(), len(line.productions()))
    
    #        print(type(line.node))
    
    #    parsed_Sentence = [parse.tree() for parse in dep_parser.raw_parse(sent)]
    #    print(parsed_Sentence)
    #
    #    for line in parsed_Sentence:
    #        print(line)
    
    




