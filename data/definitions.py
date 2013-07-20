'''
Read definitions
'''



def getDefinitions( fns = [r'data/twldefs.txt', r'data/OWLdefs.txt'] ):
    defs = {}
    for fn in fns:
        for line in open(fn,'r'):
            try:
                words, defn = line.strip().split('\t')
                for word in words.split():
                    defs.setdefault(word.lower(),defn.strip())
            except:
                #~ print line
                pass
            
            
    return defs

defn = getDefinitions()

from olddefinitions import defn as olddef
for word, exp in olddef.items():
    defn.setdefault(word,exp)
    

#~ words = 'ae um mu li za moxa'.split()
#~ for word in words:
    #~ print word, defn.get(word, 'Undefined')
