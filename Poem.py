import stanford

class Poem:
    def __init__(self, lines, pattern, rhyme_level):
        self.lines = [[] if not line else line for line in lines]
        #print('new poem()',lines)
        self.pattern = pattern
        self.rhyme_level = rhyme_level

    def __str__(self):
#        print (type(self.lines), self.lines)
#        return '\n'.join([' '.join(line) for line in self.lines])
        r = ''
        for i in range(0,len(self.lines),4):
            r += '\n'.join([' '.join(line) for line in self.lines[i:i+4]]) + '\n\n'
        return r.strip('\n')

    def __repr__(self):
        return self.__str__()

    def is_complete(self):
#        return bool(self.lines) and not len([line for line in self.lines if not line])
#        print (type(self.lines), self.lines)
        t= bool(self.lines) and len([line for line in self.lines if not line or line == [''] or line == []]) == 0
#        print (t, self.lines)
        return t

    def stats(self):
#        return(0,0)
#        return stanford.get_stats(self.__str__())
        stan_stats = [stanford.get_stats(' '.join(line)) for line in self.lines]
        return (
                sum(a for a,b in stan_stats),
                sum(b for a,b in stan_stats),
                )

# (not lines[idx] or lines[idx]==[] or lines    [idx]==[''])
    
