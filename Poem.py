import stanford
from textstat.textstat import textstat
import re
import pprint
import logging


class Poem:
    def __init__(self, lines, pattern, rhyme_level, source=''):
        self.lines = [[] if not line else line for line in lines]
        self.pattern = pattern
        self.rhyme_level = rhyme_level
        self.source = source
        self.p = re.compile(r'^\d+')
        

    def __str__(self):
        r = ''
        r += '\n'.join([
            '' if line[1] == '\n' 
            else line[1][0].capitalize() + ' ' + ' '.join(line[1][1:]) 
            for line in self.lines]) + '\n\n'
        r = r.strip('\n').strip()
        return r

    def __repr__(self):
        return self.__str__()

    def debug_string(self):
        r = ''
        #r += 'pattern = ' + pprint.pformat(self.pattern) + '\n'
        r += 'rhyme_level = ' +  pprint.pformat(self.rhyme_level) + '\n'
        r += 'source = ' + pprint.pformat(self.source) + '\n'
        r += 'is_complete() = ' + pprint.pformat(self.is_complete()) + '\n'
        r += 'score() = ' + pprint.pformat(self.score()) + '\n'
        
        r += '\n'.join([
            '' if line[1] == '\n' 
            else line[0] + ' -- ' + line[1][0].capitalize() + ' ' + ' '.join(line[1][1:]) 
            for line in self.lines]) + '\n\n'
        
        r += 'stats()' + pprint.pformat(self.stats()) + '\n'
        
        return r
        

    def is_complete(self):
#        return bool(self.lines) and not len([line for line in self.lines if not line])
#        print (type(self.lines), self.lines)
        t= bool(self.lines) and len([line for line in self.lines if line == (None,None)]) == 0
#        print (t, self.lines)
        return t
    
    def score(self):
        try:
            gs = textstat.text_standard(self.__str__())
            grade_level = int(self.p.search(gs).group(0))
            
            return (grade_level, self.rhyme_level) #return a tuple of numbers for comparison
        except Exception as e:
            logging.error('poem.score() ERROR : {0}'.format(e))
            return (0,0)


    def stats(self):
#        stan_stats = [stanford.get_stats(' '.join(line[1])) for line in self.lines]
#        return (
#                sum(a for a,b in stan_stats),
#                sum(b for a,b in stan_stats),
#                )
        r = self.__str__()
        return{
                 'textstat.flesch_reading_ease' : textstat.flesch_reading_ease(r)
                ,'textstat.flesch_kincaid_grade' : textstat.flesch_kincaid_grade(r)
                ,'textstat.smog_index' : textstat.smog_index(r)              
                ,'textstat.coleman_liau_index' : textstat.coleman_liau_index(r)
                ,'textstat.automated_readability_index' : textstat.automated_readability_index(r)
                ,'textstat.linsear_write_formula' : textstat.linsear_write_formula(r)
                ,'textstat.difficult_words' : textstat.difficult_words(r)
                ,'textstat.dale_chall_readability_score' : textstat.dale_chall_readability_score(r)
                ,'textstat.gunning_fog' : textstat.gunning_fog(r)
                ,'textstat.text_standard' : textstat.text_standard(r)
                }


    
if __name__ == '__main__':
    logFormatter = logging.Formatter("%(asctime)s : %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
#     fileHandler = logging.handlers.TimedRotatingFileHandler('Poem3.log', when='D', interval=1, backupCount=1000)
#     fileHandler.setFormatter(logFormatter)
#     logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)    
    
    
    
    p = Poem([
        ('aa',('a1','2','3')),
        ('ab',('a1','2','3')),
        ('ac',('b1','2','3')),
        ('ad',('1v','2','3')),
        ('ae',('1','aaa2','3')),
        ('af',('aaaa1','aa2','3'))
        ],[],0)
    print(p)