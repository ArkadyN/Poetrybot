import stanford
import itertools

class Poem:
    def __init__(self, grams, pattern, rhyme_level):
#        self.lines = [[] if not line else line for line in lines]
        self.grams = grams
        self.lines = [list(g) for k,g in itertools.groupby(self.grams,lambda x: x=='EOL') if not k]
#        print('new poem()',grams)
        self.pattern = pattern
        self.rhyme_level = rhyme_level

    def __str__(self):
        print (type(self.lines), self.lines)
#         [[['Return'], ['types'], ['\n']]]
         
        return ' '.join(list(Poem._flatten(self.grams)))

    def __repr__(self):
        return self.__str__()

    def is_complete(self):
        t= bool(self.grams) and len([gram for gram in self.grams if not gram or gram == '']) == 0
        return t

    def stats(self):
#        return stanford.get_stats(self.__str__())
        stan_stats = [stanford.get_stats(' '.join(line)) for line in self.__str__().split('\n')]
        return (
                sum(a for a,b in stan_stats),
                sum(b for a,b in stan_stats),
                )

# (not lines[idx] or lines[idx]==[] or lines    [idx]==[''])
    
    def _flatten(container):
        for i in container:
            if isinstance(i, (list,tuple)):
                for j in Poem._flatten(i):
                    yield j
            else:
                yield i 
