#!/usr/bin/env python
""" Console for Scrabble
    There are no debug test cases yet.
"""
import cmd
#import readline

from lib.dawg import lexicon, showTiles, print_lines
from data.definitions import defn

class scrabbleConsole ( cmd.Cmd ):
    def __init__(self, lex):
        # cmd.Cmd.__init__(self,lex)
        cmd.Cmd.__init__(self)
        self.intro = "Welcome to kiddle's diddle"
        self.prompt = '-=> '
        self._hist = []
        self.lex = lex

    ## Command definitions ##
    def do_hist(self, args):
        """ list of previously entered commands"""
        print self._hist

    def do_exit(self,args): 
        """ Quit the console."""
        return -1

    def do_quit(self,args):
        """ Quit the console."""
        return self.do_exit(args)

    def do_EOF(self,args):
        """ Quit the console."""
        return self.do_exit(args)

    def do_a(self,args): 
        """a <tiles>
        Find all legal words that can be constructed from <tiles>
        Ex: a pear
        """
        try:
            args = args.split()
            print_lines(self.lex.anagram(args[0]))
        except Exception, e:
            print e
            print 'Incorrect number of arguments:\n\ta <tiles>'

    def do_l(self,args):
        """l <word>
        Look up the definition of a word.
        """
        word = args.split()[0]
        if not self.lex.isValid(word):
            print '%s is not a valid word.' % word
            return
            

        expl = defn.get(word, 'Sorry, undefined')
        print '%s: %s'%(word, expl)

    def do_m(self,args): 
        """m <pattern> <tiles>
        Find all legal words that can be constructed from <pattern> and <tiles>
        A pattern can have '*' or '?' where:
            ? : matches exactly one character
            * : matches zero or more characters
        Ex: m pear? seat
        
        Returns: pear(s), pear(t)
        """
        try:
            args = args.split()
            print_lines(self.lex.match(args[0], args[1]))
        except Exception, ex:
            print ex
            print 'Incorrect number of arguments:\n\tm <pattern> <tiles>'

    def do_v(self,args): 
        """v <word>
        Verify if <word> is a legal word
        Ex: v xis
        """
        try:
            args = args.split()
            res = 'NOT valid'
            if self.lex.isValid(args[0]):
                res = 'valid'
            print '%s is %s'%(args[0],res)

        except:
            print 'Incorrect number of arguments:\n\tv <word>'

    def do_b(self,args): 
        """b <pattern> <tiles>
        Find words that can fit at the bottom
        Ex: b hello pale 
        Ex: b hi en s pale
                he
                ins
        ------------- <-- insert pale
        """
        try:
            args = args.split()
            pattern, rack = list(args[0]), args[-1]
            patternShow = pattern
            if len(args) > 2:
                pattern = args[:-1]
                patternShow = '.'.join(pattern)

            res = self.lex.findride(pattern, rack, False)
            #print res
            if res == []:
                print 'No matches'
            else: 
                showTiles(patternShow, res ,True)
        except Exception,e:
            print 'Incorrect number of arguments:\n\tb <pattern> <tiles>'
            print e

    def do_t(self,args): 
        """t <pattern> <tiles>
        Find words that can fit at the top of <pattern>
        Ex: v xis
        """
        try:
            args = args.split()
            pattern, rack = list(args[0]), args[-1]
            patternShow = pattern
            if len(args) > 2:
                pattern = args[:-1]
                patternShow = '.'.join(pattern)

            res = self.lex.findride(pattern, rack, True)
            if res == []:
                print 'No matches'
            else: 
                showTiles(patternShow, res ,False)
        except Exception,e:
            print 'Incorrect number of arguments:\n\tt <pattern> <tiles>'
            print e

    def do_help(self, args):
        """Get help on commands
        'help' or '?' with no arguments prints a list of commands for which help is available
        'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this mmethod is for the help text in the doc string
        cmd.Cmd.do_help(self,args)

    ## Override medhods in Cmd Object
    def preloop(self):
        cmd.Cmd.preloop(self)
        self._hist = []

    def postloop(self):
        cmd.Cmd.postloop(self)
        print 'exiting...'

    def precmd(self, line):
        self._hist += [line.strip()]
        return line

    def preloop(self):
        print "Don't cheat..."

lex = lexicon()
print 'Please wait while loading dictionary'
print 'Using The Official Word List of 2006 (twl06)'
lex.loadfile(r'data/twl06.txt')
print 'Done!\n'
try:
    console = scrabbleConsole(lex)
    console.cmdloop()
except AttributeError, e: 
    print e
