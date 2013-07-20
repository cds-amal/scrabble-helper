#!/usr/bin/env python
"""
This is the "Directed-Acyclic-Graph" module.
"""
from string import uppercase
from string import lowercase

## to calculate console size
from os import popen

## These variables are for pruning the DAWG for efficiency
g_node_counter  = 0

def uniq(alist):
    """Return a unique list
    >>> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    >>> uniq(l)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    """
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]

def flatten(list): return [a for sublist in list for a in sublist]

from string import uppercase as UPC
def isAnagram( w, tiles):
    """ Returns true if w is an anagram of rack"""
    rack = tiles[:]
    for l in w:
        if l in rack:
            rack = rack.replace(l,'',1)
        elif l in UPC and '?' in rack:
            rack = rack.replace('?','',1)
        else: return False
    return True

def per(lol, wrd=''):
    """ Helper function for permute"""
    try:
        start = lol[0]
    except: start = []
    
    for i in start:
        yield wrd+i

        itr = per(lol[1:], wrd+i)
        for rest in itr:
            yield rest
    raise StopIteration


    
def permute(lol, rack):
    """ Return a dictionary of words.
    Examples:
    
    >>> permute ( [ ['a'], ['b'], ['c'] ], 'abc' )
    {0: ['a', 'ab', 'abc'], 1: ['b', 'bc'], 2: ['c']}
            
    >>> permute ( [ ['a', 'e'], ['a','p'], ['a','e'], ['a','e'], ['l'] ], 'pale' ) 
    {0: ['a', 'ap', 'ape', 'e', 'ea', 'ep', 'epa'], 1: ['a', 'ae', 'p', 'pa', 'pae', 'pael', 'pe', 'pea', 'peal'], 2: ['a', 'ae', 'ael', 'e', 'ea', 'eal'], 3: ['a', 'al', 'e', 'el'], 4: ['l']}
            
    There might be a blank (?) in the rack. The ? can match any letter.

    >>> d = permute ( [ ['a','H'], ['E','O','b'], ['T','e','f'], ['a','O']], 'abef?' )
    >>> d[0]
    ['a', 'aE', 'aEe', 'aEf', 'aO', 'aOe', 'aOf', 'ab', 'abT', 'abe', 'abeO', 'abf', 'abfO', 'H', 'Hb', 'Hbe', 'Hbea', 'Hbf', 'Hbfa']
    
    >>> d[1]
    ['E', 'Ee', 'Eea', 'Ef', 'Efa', 'O', 'Oe', 'Oea', 'Of', 'Ofa', 'b', 'bT', 'bTa', 'be', 'bea', 'beO', 'bf', 'bfa', 'bfO']
    
    >>> d[2]
    ['T', 'Ta', 'e', 'ea', 'eO', 'f', 'fa', 'fO']
    
    >>> d[3]
    ['a', 'O']

    >>> d = permute( [ [], ['n'], ['l','m','n'], ['i','o']], 'oiomlni')
    >>> d[0]
    []
    >>> d[1]
    ['n', 'nl', 'nli', 'nlo', 'nm', 'nmi', 'nmo']
    >>> d[2]
    ['l', 'li', 'lo', 'm', 'mi', 'mo', 'n', 'ni', 'no']
    >>> d[3]
    ['i', 'o']
    
    Sometimes empty lists have to be considered

    >>> permute ([['a'],[], ['b','a'], ['d']], 'bad')
    {0: ['a'], 1: [], 2: ['b', 'bd', 'a', 'ad'], 3: ['d']}
    """
    
    lst = []
    for i in range(len(lol)):
        itr = per(lol[i:])
        lst.append( (i, [x for x in itr if isAnagram(x, rack)]))
    return dict(lst)
    
    
def showTiles( header, words, bottomview=True ):
    """
    Examples:
    
    ** Note to testwriters:
            There is a trailing blank on each line of output
    
     showTiles( 'hello', [(0,'e')], False)
    [e]
    [h] [e] [l] [l] [o]

     showTiles( 'hello', [(0,'ale')], False)
    [a]-[l]-[e]
            [h] [e] [l] [l] [o]

     showTiles( 'hello', [(0,'ape')], False)
    [a]-[p]-[e]
            [h] [e] [l] [l] [o]

     showTiles( 'hello', [(1,'p')], False)
        [p]
    [h] [e] [l] [l] [o]

     showTiles( 'hello', [(1,'pa')], False)
        [p]-[a]
    [h] [e] [l] [l] [o]

     showTiles( 'hello', [(1,'peal')], False)
        [p]-[e]-[a]-[l]
    [h] [e] [l] [l] [o]

    showTiles( 'hello', [(4,'la')], False)
                    [l]-[a]
    [h] [e] [l] [l] [o]
    """
    # make a grid first
    # find max height
    maxh = 1
    if '.' in header:
        maxh = max([len(x) for x in header.split('.')]) 
    
    # find width
    maxw = max( [ len(i[1]) for i in words])
    
    # construct #rid
    if bottomview:
        # make  a list of  words
        #     [ [a b c] [d e f] [g h i] ]
        if '.' in header:
            tlist = [ list(w) for w in header.split('.')]
            listx = [ ''.join(r).rjust(maxh) for r in tlist ]
            lines = []
            for a in range(maxh):
                lines.append( ''.join(['[%s] '%w[a] for w in listx]))
        else:
            lllines = [ '[%s] '%c for c in header]
            lines = [ ''.join(lllines) ]
    else:
        # make  a list of reversed words
        #     [ [a b c] [d e f] [g h i] ]
        if '.' in header:
            tlist = [list(w) for w in header.split('.')]
            for r in tlist: r.reverse()
                
            pad = [ ''.join(r).rjust(maxh) for r in tlist ]    
            lines = []
            for a in range(maxh):
                lines.append(''.join(['[%s] '%w[a] for w in pad]))
            lines.reverse()
        else:
            lllines = [ '[%s] '%c for c in header]
            lines = [ ''.join(lllines) ]

    # A word is specified in the tuple (pos, word) where pos is a signed int
    for pos, wrd in words:

        # space before header (preheader) & space before word (preword)
        preheader, preword = 0,0
        
        # if pos is < 0 then you need to prepend spaces.
        if pos < 0:
            preheader = 4 * abs(pos)
        else:
            preword = 4 * pos
                
        ln = ''.join([ '[%s]-'%l for l in wrd ])[:-1]
        
        # print header
        if bottomview:
            for l in lines: print l.rjust(len(l) + preheader)
    
        print ln.rjust(len(ln) + preword)
        
        if not bottomview:
            for l in lines: print l.rjust(len(l) + preheader)
        print
                
                        
def print_lines(alist, retularOuput=True):
    """Print out 1 letter words, then 3 , then 4 etc..."""
    
    rows, columns = popen('stty size', 'r').read().split()
    row = ''
    try:
        rows, columns = int(rows), int(columns)
        columns = columns/2
    except:
        rows, columns = 10, 80
    for l in range(1, 16):
        sub = [ x for x in alist if len(x.replace('<','').replace('>','')) == l ]
        if len(sub) > 0 :
            row = ''
            for w in sub:
                # print row
                if row == '':
                    row = '%02d: %s'%(l, w)
                else:
                    frag = ' %s' % w
                    if len(frag) + len(row) > columns:
                        print row
                        row = '%02d: %s' %(l, w)
                    else:
                        row += frag
        if row:
            print row
            row = ''
                
class node:
    """ A node to be used in a DAC"""
    
    def __init__(self, a, eow=False):
        global g_node_counter
        self.letter, self.eow, self.next = a, eow, {}
        g_node_counter += 1
        
    def __del__(self):
        global g_node_counter
        g_node_counter -= 1
        
    def __eq__(self, rhs):
        """ compare two nodes """
        if self.letter != rhs.letter: return False
        lkeys = self.next.keys()
        lkeys.sort()
        rkeys = rhs.next.keys()
        rkeys.sort()
        if lkeys != rkeys: return False

        for letter, n in self.next.items():        
            try: return n == rhs.next[letter]
            except: return False
        return True
        
    def __ne__(self,rhs):
        pass
    
    def insert(self, word):
        """ Insert word into the dag."""
        
        curr, append = self, False
        for l,dx in zip (word, range(len(word))):
            if l in curr.next:
                curr = curr.next[l]
            else:  
                start, append = dx, True
                break
                        
        if append:
            for l in word[start:]:
                curr.next.setdefault(l,node(l))
                curr = curr.next[l]        
        curr.eow = True
        
    def isValid(self, word):
        curr = self
        for l in word:
            if l in curr.next: 
                curr = curr.next[l]
            else: return False      
        return curr.eow

    def _walk(self, wordbuf='', lst=[]):
        word = wordbuf + self.letter
        if self.eow:
            lst.append(word)
        
        for n in self.next.values():
            n._walk(word,lst)
        
    def _find_leaf_nodes(self, dic, parent):
        """Helper function to find all leafnodes in a dawg"""
        if self.next == {}:
            l = dic.setdefault(self.letter,[self]) # 1st time wil store self as 1st entry
            l.append(parent)
        else:
            for n in self.next.values():
                n._find_leaf_nodes(dic, self)
                        
    def _find_leaf_nodes_level1(self, dic, parent):
        """Helper function to find all nodes with 1 child"""
        if len(self.next) == 1:
            key = '%s%s'%(self.letter, self.next.values()[0].letter)
            l = dic.setdefault(key,[self]) # 1st time will store self as 1st entry
            l.append(parent)
        else:
            for n in self.next.values():
                n._find_leaf_nodes_level1(dic, self)
                        
    def match(self, pattern, word, tiles, lst, matchedonblank):
        """Find all words that match the pattern that can be made from tiles"""
    
        if matchedonblank:
            wordbuf = word + self.letter.upper()
        else:
            wordbuf = word + self.letter

        # when matching a star:
        # *<word> 
        #       match *eas    -> the added words have to end in 'eas'
        if len(pattern) == 1 and pattern[0] == '*':
            if self.eow:
                lst.append(wordbuf)
                        
        if pattern == '':
            if self.eow: 
                lst.append(wordbuf)
            return
    
        # match next character in pattern
        if pattern[0] == '*':
            if '?' in tiles:
                # go thru all the next-nodes but don't change the search pattern
                for l in self.next.values():
                    l.match(pattern, wordbuf, tiles.replace('?','',1), lst, True)
            if len(tiles) > 0:        
                for l in [ x for x in self.next.values() if x.letter in tiles ]:
                    l.match(pattern, wordbuf, tiles.replace(l.letter,'',1),lst,False)
            
            if len(pattern) > 1:
                exit_letter = pattern[1]
                if exit_letter in self.next:
                    self.next[exit_letter].match(pattern[2:], wordbuf, tiles, lst, False )
                        
        elif pattern[0] == '?': 
                # check if blank in tiles
                if '?' in tiles:
                    for l in self.next.values():
                        l.match(pattern[1:], wordbuf, tiles.replace('?','',1), lst, True)
                for l in [ x for x in self.next.values() if x.letter in tiles ]:
                    l.match(pattern[1:], wordbuf, tiles.replace(l.letter,'',1), lst, False)
        else:
                # does this next patern character match a word?
                if pattern[0] in self.next:
                    self.next[pattern[0]].match(pattern[1:], wordbuf, tiles, lst, matchedonblank=False)
        
    def findWords(self, word, tiles, lst, matchedonblank):
        if matchedonblank:
            wordbuf = word + self.letter.upper()
        else:
            wordbuf = word + self.letter
        
        if self.eow: lst.append(wordbuf)
    
        if '?' in tiles:
            for l in self.next:
                self.next[l].findWords(wordbuf, tiles.replace('?','',1),lst,matchedonblank=True)
    
        for l in tiles.replace('?',''):
            if l in self.next:
                self.next[l].findWords(wordbuf, tiles.replace(l,'',1), lst, matchedonblank=False)
    
    
class dawg:
    """A directed Acyclic Word Graph"""
    
    def __init__(self, ltr):
        self.node = node(ltr)
    
    def insert(self, word):
        """insert word into the dawg"""
        self.node.insert(word)
    
    def getwords(self):
        """return a list of all the words in the dag"""
        thelist = []
        self.node._walk(lst=thelist)
        return thelist
    
    def findWords(self, t, matchedonblank=False):
        thelist = []
        self.node.findWords(tiles=t, word='', lst = thelist, matchedonblank=matchedonblank)
        return thelist
    
    def match(self, p, t, matchedonblank=False):
        thelist = []
        self.node.match(pattern=p, word='', tiles=t, lst = thelist, matchedonblank=matchedonblank)
        return thelist
    
    def isValid(self, word):
        return self.node.isValid(word)
    
    def find_leaf_nodes(self, dic):
        self.node._find_leaf_nodes(dic, self)
        
    def find_leaf_nodes_level1(self, dic):
        self.node._find_leaf_nodes_level1(dic,self)
    
from string import lowercase  
    
class lexicon:
    """ 
    This is the lexicon object. It contains the root nodes for all the 
    Directed-Acyclic-Word-Graphs.
    """
    
    def __init__(self):
        """ Create a new lexicon """
        self.dag, self.wordcount = {}, 0
        for l in lowercase:
            self.dag.setdefault(l, dawg(l))

    def importFromDict(self, dic ):
        for word in dic.keys():
            if '-' in word: continue
            self.insert(word.lower().strip())
        print 'added hack:\nWords from definition'
        
    def insert(self, word):
        """ Insert a new word into the dictionary """
        # Call the correct root node as the starting point
        self.dag[word[0]].insert(word[1:])
        self.wordcount += 1
    
    def loadfile(self, fn):
        """ Populate the lexicon from a file. """
        fi = open(fn,'r')
        for l in fi.readlines():
            if l[0] == '#': continue
            self.insert(l.lower().strip())
        fi.close()
        print '%d nodes were used for %d words'%(g_node_counter, self.wordcount)
        
    def isValid(self, word):
        word = word.lower()
        #print 'checking %s'%word
        return self.dag[word[0]].isValid(word[1:])

    def anagram(self, tiles):
        """"Make a list of valid words from tile letters."""
        lst = []
    
        if '?' in tiles:
            for l in lowercase:
                lst += self.dag[l].findWords(tiles.replace('?','',1), matchedonblank=True)
    
        for l in tiles.replace('?',''):
            lst += self.dag[l].findWords(tiles.replace(l,'',1), matchedonblank=False)    
        
        return uniq(lst)

    def match(self, pattern, tiles):
        """Find the list of words that match the pattern. Wildcard is ?"""
        lst = []
        pattern = pattern.lower()
        first = pattern[0]
        if first == '?':
            if '?' in tiles:
                for l in lowercase:
                    lst += self.dag[l].match(pattern[1:], tiles.replace('?','',1),matchedonblank=True)
            for l in [x for x in lowercase if x in tiles]:
                lst += self.dag[l].match(pattern[1:], tiles.replace(l,'',1), matchedonblank=False)
                                                
        elif first == '*':
            if '?' in tiles:
                for l in lowercase:
                    lst += self.dag[l].match(pattern, tiles.replace('?','',1), matchedonblank=True)
            for l in [x for x in lowercase if x in tiles]:
                lst += self.dag[l].match(pattern, tiles.replace(l,'',1), matchedonblank=False)
            if pattern[-1] == '*': # is this case necessry? TODO
                lst += self.match(pattern[1:], tiles)
                lst += self.match(pattern[:-1], tiles)
                                
        else:
            # eat the first character from the pattern.
            lst += self.dag[first].match(pattern[1:], tiles, matchedonblank=False)
                        
        return uniq(lst)
                
    def trimLeaves(self):
        global g_node_counter
        dic = {}
        for n in self.dag.values():
            n.find_leaf_nodes(dic)

        for l,lst in dic.items():
            for anode in lst[1:]:      # use 1st item in list as the proper node
                anode.next[l] = lst[0] 
        
        print 'nodes trimmed by %d'% g_node_counter
        
    def isValidRider( self, wdef, pattern, top=True):
        pos, word = wdef
        #print wdef, pattern
        if len(word) == 1 and pattern[pos] != '-' : return True
        # make sure word is valid
        if self.isValid(word) == False: return False

        if pos < 0:
            pos = -pos
            chk = zip (word[pos:], pattern)
        elif pos > 0:
            chk = zip(word, pattern[pos:])
        else: chk = zip(word, pattern)   
        
        for w,p in chk:
            if p == '-': continue
            if top:
                if not self.isValid(w+p): return False
            else: 
                if not self.isValid(p+w): return False
                
        return True

    def findride(self, pattern, tiles, top=True):
        """ find all the possible words that can sit on top of pattern.
        @ return [ (pos, word) ...]
        
        A list of tuples denoting the relative position of target word in relation to pattern.
        
        For example, findride( 'hello', 'pale' ) returns 'pale' in its list.
        : ( pos, word ) where position is an signed integer denoting how far to the left (-)
        : or right (+) to place the word.
        : (2, 'pale')
        :         [p] [a] [l] [e] 
        : [h] [e] [l] [l] [o]
        :
        : (-3, 'pale')
        : [p] [a] [l] [e] 
        :             [h] [e] [l] [l] [o]
        b ag.ti.t stiebol <-- fails , doesn't find tile under ti
        """
        
        # get the 2 letter words that fit on top or bottom
        mstring, matchall, mchar = '%s?', '-%s', -1  #bottom
        if top == True:
            mstring, matchall, mchar = '?%s', '%s-', 0 #top

        zipped = zip(range(len(pattern)),pattern)    
        dic = {}
        for dx,let in zipped:
            if let == '-': # matches anything
                m = [ matchall%c for c in tiles ]
            else:
                m = self.match(mstring%let, tiles)
            lst = [x[mchar] for x in m]
            dic.setdefault( dx, lst)

        retval = []
        dic = permute( [ x for x in dic.values()], tiles)
        for k,v in dic.items(): retval += [(k,i) for i in v]
        
        # find extend words in the beginning and end positions
        alist = []
        for word in dic[0]:
            rack = tiles[:]
            
            # TODO keeping track of uppercase looks fishy. investigate and change
                
            # replace letters to do extension search.
            for l in word:
                if l in uppercase:
                    rack, makeupper = rack.replace('?','',1), True
                else:
                    rack, makeupper = rack.replace(l,'',1), False
                
            # get all words by prepending whatever's possible    
            x = self.match('*%s' % word, rack)
                
            # Replace the Uppercase character
            if makeupper:
                x = [ q.replace(word.lower(), word,1) for q in x]
            # remove current word from matched list because *<word> includes <word> solution
            try: x.remove(word)
            except: pass

            # Construct return entry tuple
            alist += [(-i.rfind(word), i) for i in x]
            #print alist
            
            # match *word*
            if len(word) == len(pattern):
                x = self.match('*%s*'% word, rack)
                if makeupper:
                    x = [ i.replace(word.lower(), word,1) for i in x]
            # remove current word from matched list because *<word> includes <word> solution
            try: x.remove(word)
            except: pass
            xx = []
            for i in x:
                pos = i.find(word)
                if pos > 0: pos = -pos
                xx.append( (pos, i))
                alist += xx
        retval += alist
        
        # process words that are between the 1st and last characters
        for dx in range(1, len(pattern)-1):
            alist,x = [],[] 
            for word in dic[dx]:
                rack = tiles[:]
                for l in word:
                    if l in uppercase:
                        rack, makeupper = rack.replace('?','',1), True
                    else:
                        rack, makeupper = rack.replace(l,'',1), False

                if len(word) == len(pattern)-dx:
                    x = self.match('%s*'% word, rack)
                    if makeupper:
                        x = [ i.replace(word.lower(), word, 1) for i in x ]
                        try: x.remove(word)
                        except: pass
                    alist += [ ( dx, i) for i in x ]
            retval += alist        
                
        alist, x = [],[]
        lastindex = len(pattern)-1
        for word in dic[lastindex]:
            rack = tiles[:]
            for l in word:
                if l in uppercase:
                    rack, makeupper = rack.replace('?','',1), True
                else:
                    rack, makeupper = rack.replace(l,'',1), False

                x = self.match('%s*'%word,rack)
                if makeupper:
                    x = [i.replace(word.lower(), word, 1) for i in x ]
                try: x.remove(word)
                except: pass

                alist += [ (lastindex, i) for i in x]
        retval += alist
        retval = uniq(retval)
        retval.sort()
        retval = [ i for i in retval if len(i) == 1 or self.isValidRider(i,pattern,top) ]
        return retval
        
def test_single_dawg():
    print 'test single dawg'  
    words = 'aa aah aahs able abouts about' 
    dag = dawg('a')
    for w in words.split():
        dag.insert( w[1:])
    print '%d nodes were used.'%g_node_counter
    print 'getting words...'
    l = dag.getwords()
    print l
    
    vdict = { True : 'valid', False : 'invalid' }
    words = 'aa aav aah aeh aboutz abouts about'
    for w in words.split():
        print '%s is %s' %(w, dag.isValid(w[1:]))
    print 'done single dawg'  
    

def test_match_001():
    """ 
    Node properties:
    ================
    
    1. Equality
    ----------
        >>> n1, n2 = node('a'), node('a')

    Identity:
        >>> n1 == n1
        True
        >>> n2 == n2
        True
    
        >>> n1 == n2
        True
        >>> n2 == n1
        True
    
        >>> n1, n2 = node('a'), node('b')
        >>> n1 == n2
        False
        >>> n2 == n1
        False
    
    Equality with children
        >>> n1, n2, n3 = node('a'), node('a'), node('a')
        >>> words =[ 'able', 'abide', 'abet' ]
        >>> n1.insert(words[0]) 
        >>> n1.insert(words[1]) 
        >>> n1.insert(words[2]) 
        >>> n2.insert(words[1]) 
        >>> n2.insert(words[2]) 
	>>> n1 == n2
	False
        >>> words = ['arid', 'are', 'area']
        >>> n3.insert(words[0]) 
        >>> n3.insert(words[1]) 
        >>> n3.insert(words[2]) 
	>>> n1 == n3
	False
	>>> n2 == n3
	False

    Matching tests
    dag = lexicon()
	 dag.loadfile('word.lst')
	389337 nodes were used for 173528 words
	 dag.match('?wo', '?' )
	['Two']

    t rave datgoq?
    b r.no.jap.i names    (names should be returned [r]n<ames )
    b are.breed ntihiid   - dumps
    b d.wi.or.t.i.e eealaao   - bad word wie
    m ?wo ? does't get 'two'
    m *a ????   doesn't return anything -- fixed - add test
    b fez.o.a etoigun  doesn't match ego oe,ag + o
    """

def _test():
    import doctest, dawg
    return doctest.testmod(dawg, verbose=True)

if __name__ == '__main__':
    _test()   
