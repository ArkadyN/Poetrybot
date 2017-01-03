import wikipedia 
from RoboPoet import RoboPoet
from Poem import Poem
import pprint
from datetime import datetime
import logging




def get_best_poem(phrases):
    poems = []
    for phrase in phrases:
        ps = get_best_poem_2(phrase)
        if ps:
            poems.append(ps)
    
    if len(poems):
        return sorted(poems, key=lambda poem: poem.score(), reverse=True)[0]
    else:
        return None


def get_best_poem_2(phrase):
    page = None
    
    p = phrase
    for i in range(10):
        try:
            page = wikipedia.page(p)
            if page:
                break
        except wikipedia.exceptions.DisambiguationError as e:
            logging.info('wiki.get_best_poem_2() disambiguation {0}'.format(phrase))
            p = e.options[0]
        except Exception as e:
            logging.error('wiki.get_best_poem_2() ERROR : {0} {1}'.format(phrase, e))
            break
                  
#     try:
#         page = wikipedia.page(phrase)
#     except wikipedia.exceptions.DisambiguationError as e:
#         logging.info('wiki.get_best_poem_2() disambiguation {0}'.format(phrase))
#         page = wikipedia.page(e.options[0])
#     except Exception as e:
#         logging.error('wiki.get_best_poem_2() ERROR : {0} {1}'.format(phrase, e))
#         pass
     
    if page:
        logging.info('wiki.get_best_poem_2() phrase : {0} page.tile : {1}'.format(phrase,page.title))
        r = RoboPoet(text=page.content)
        poem = r.get_best_poem()
        if poem:
            poem.source = page.title
            return poem
    
    return None



if __name__ == '__main__':
    
    logFormatter = logging.Formatter("%(asctime)s : %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
#     fileHandler = logging.handlers.TimedRotatingFileHandler('wiki.log', when='D', interval=1, backupCount=1000)
#     fileHandler.setFormatter(logFormatter)
#     logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)           
    
    
    
    words = [
            'OSU'
#             ,'OSU campus' 
            ,'campus'
        
#             'new york'
#             ,'favorites'
#             ,'cat'
# #            ,'bastards'
#             ,'america'
#             ,'linear algebra'
# #            ,'the ottomans'
#             ,'on the town'
#             ,'broadway'
#             ,'musical'
#             ,'New York Stock Exchange'
#             ,'Stock exchange'
#             ,'Jakarta Mass Rapid Transit'
#             ,'Hollywood'
#             ,'Film'
#             ,'hello','see','woman','pop'
            ]
    for word in words:
        print('\n\n\n\n')
        print(datetime.now(), '-'*20)
        print(word)

        best_poem = get_best_poem_2(word)
        if best_poem:
            print(best_poem.debug_string())
        else:
            print('Got None')

# #        r = RoboPoet(text='')
# #        print(datetime.now(), r.list_of_rhymes(word,4))
# #        print(datetime.now(), r.list_of_rhymes_2(word,4))
# #        print(datetime.now(),  sorted(list(r.list_of_rhymes(word,4))) == sorted(list(r.list_of_rhymes_2(word,4)))  )
# #        continue
# 
#         try:
#             page = wikipedia.page(word)
#         except wikipedia.exceptions.DisambiguationError as e:
#             page = wikipedia.page(e.options[0])
#         except Exception as e:
#             print(e)
#             continue
# 
#         print(page.title)
# 
#         r = RoboPoet(text=page.content
# #                ,min_rhyme_level=1
# #                ,max_rhyme_level=2
#                 )
# #        print('haiku \n', pprint.pformat(r.get_poem(RoboPoet.pattern_haiku, rhyme_level=4)))
# #        print('haiku \n', pprint.pformat(r.get_poem(RoboPoet.pattern_haiku_rhymed, rhyme_level=4)))
#         #print('other', pprint.pformat(r.get_poem(RoboPoet.patterns[1])))
#         #print('other', pprint.pformat(r.get_poems()))
# 
# #         for poem in r.get_poems():
# #             print(datetime.now(), '='*10)
# #             print(poem.pattern, poem.rhyme_level, poem.is_complete(), poem.stats(), '\n', poem.to_string())
# 
#         best_poem = r.get_best_poem()
#         if best_poem:
#             print(best_poem.to_string())
#             print(best_poem.score(), best_poem.rhyme_level)





