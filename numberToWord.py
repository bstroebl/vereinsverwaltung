# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''Convert number to English words
$./num2eng.py 1411893848129211
one quadrillion, four hundred and eleven trillion, eight hundred and ninety 
three billion, eight hundred and forty eight million, one hundred and twenty 
nine thousand, two hundred and eleven
$
 
Algorithm from http://mini.net/tcl/591
Source: http://www.blog.pythonlibrary.org/2010/10/21/python-converting-numbers-to-words/
'''
 
# modified to exclude the "and" between hundreds and tens - mld
 
__author__ = 'Miki Tebeka <tebeka@cs.bgu.ac.il>'
__version__ = '$Revision: 7281 $'
 
# $Source$
 
import math
 
# Tokens from 1000 and up
_PRONOUNCE = [ 
    'million',
    'tausend',
    ''
]
 
# Tokens up to 90
_SMALL = {
    '0' : '',
    '1' : 'eins',
    '2' : 'zwei',
    '3' : 'drei',
    '4' : 'vier',
    '5' : u'fünf',
    '6' : 'sechs',
    '7' : 'sieben',
    '8' : 'acht',
    '9' : 'neun',
    '10' : 'zehn',
    '11' : 'elf',
    '12' : u'zwölf',
    '13' : 'dreizehn',
    '14' : 'vierzehn',
    '15' : u'fünfzehn',
    '16' : 'sechzehn',
    '17' : 'siebzehn',
    '18' : 'achtzehn',
    '19' : 'neunzehn',
    '20' : 'zwanzig',
    '30' : 'dreissig',
    '40' : 'vierzig',
    '50' : u'fünfzig',
    '60' : 'sechzig',
    '70' : 'siebzig',
    '80' : 'achtzig',
    '90' : 'neunzig'
}
 
def get_num(num):
    '''Get token <= 90, return '' if not matched'''
    return _SMALL.get(num, '')
 
def triplets(l):
    '''Split list to triplets. Pad last one with '' if needed'''
    res = []
    for i in range(int(math.ceil(len(l) / 3.0))):
        sect = l[i * 3 : (i + 1) * 3]
        if len(sect) < 3: # Pad last section
            sect += [''] * (3 - len(sect))
        res.append(sect)
    return res
 
def norm_num(num):
    """Normelize number (remove 0's prefix). Return number and string"""
    n = int(num)
    return n, str(n)
 
def small2word(num):
    '''English representation of a number <= 999'''
    n, num = norm_num(num)
    hundred = ''
    ten = ''
    if len(num) == 3: # Got hundreds
        hundred = get_num(num[0]) + 'hundert'
        num = num[1:]
        n, num = norm_num(num)
    if (n > 20) and (n != (n / 10 * 10)): # Got ones
        tens = get_num(num[0] + '0')
        ones = get_num(num[1])
        ten = ones + 'und' + tens
    else:
        ten = get_num(num)
    if hundred and ten:
        return hundred  + ten
        #return hundred + ' and ' + ten
    else: # One of the below is empty
        return hundred + ten
 
#FIXME: Currently num2eng(1012) -> 'one thousand, twelve'
# do we want to add last 'and'?
def num2word(num):
    '''English representation of a number'''
    num = str(long(num)) # Convert to string, throw if bad number
    if (len(num) / 3 >= len(_PRONOUNCE)): # Sanity check
        raise ValueError('Number too big')
 
    if num == '0': # Zero is a special case
        return 'Null'
 
    # Create reversed list
    x = list(num)
    x.reverse()
    pron = [] # Result accumolator
    ct = len(_PRONOUNCE) - 1 # Current index
    for a, b, c in triplets(x): # Work on triplets
        p = small2word(c + b + a)
        if p:
            pron.append(p + _PRONOUNCE[ct])
        ct -= 1
    # Create result
    pron.reverse()
    return ''.join(pron)
 
if __name__ == '__main__':
    from sys import argv, exit
    from os.path import basename
    if len(argv) < 2:
        print 'usage: %s NUMBER[s]' % basename(argv[0])
        exit(1)
    for n in argv[1:]:
        try:
            print num2word(n)
        except ValueError, e:
            print 'Error: %s' % e
