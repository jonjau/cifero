#June 2018

'''
cifero.translit

syll() is the main function here. It separates syllables in a given IPA word.
'''

import re

import cifero.sheets as sheets

# pbtdkgθðfvszʦʃʒʧʤhxɲnmŋlɹrjwʔɑaɪiʊuɛeoɔəʌæ

ipa_cons = list(filter(None, sheets.ipa_sheet['consonants']))
ipa_vows = list(filter(None, sheets.ipa_sheet['vowels']))

# matches valid consonant clusters or consonants for next syll in cons bl
c_re = re.compile(r'''
                    \b(?P<a>\w*?)(?P<b>{0})\b
                    '''
                    .format('|'.join(sheets.vcc + ipa_cons)), re.X)

# matches leftmost adjacent vowel and consonant blocks
vc_re = re.compile(r'''
                    \b(?P<v>[{1}]+)(?P<c>[{0}]+)(?=[{1}]+)
                    '''
                    .format(''.join(ipa_cons),''.join(ipa_vows)), re.X)

# matches any vowel and consonant blocks in a word
anyblocks_re = re.compile(r'''
                        ([{0}]+|[{1}]+)
                        '''
                        .format(''.join(ipa_cons),''.join(ipa_vows)), re.X)

# matches consonant blocks at the ends of a word
ends_re = re.compile(r'''
                        \b(?P<f>[{0}]*)
                        (?P<m>[{1}]*\w*?[{1}]*)
                        (?P<b>[{0}]*)\b
                        '''
                        .format(''.join(ipa_cons),''.join(ipa_vows)), re.X)

# matches punctuation marks at the ends of a word
# can't use marks from tabula.py because of escaping issues
# marks = :;,.!?[](){}"'<>
marks_re = re.compile(r'''
                        ^(?P<f>[:;,.!?[\](){{}}"'<>]*)
                        (?P<m>[{0}]*)
                        (?P<b>[:;,.!?[\](){{}}"'<>]*)$
                        '''
                        .format(''.join(ipa_cons + ipa_vows)),re.X)

# matches standalone symbols, also escaping issues
# &#$%@= reserved for Key
symbols_re = re.compile(r'''^[*+\-/~]$''')


def cut_m(word):
    '''returns dict of front(f), middle(m), back(b) part of the word, the
    ends being the punctuation marks at the ends.'''
    marks = re.search(marks_re, word)
    if marks:
        return marks.groupdict()
    else:
        print(word)
        print('Invalid marks at the ends of the word. Uncuttable')
        return


def is_symbol(symbol):
    '''checks if "word" is actually a standalone symbol.'''
    symbol = re.match(symbols_re, symbol)
    if symbol:
        return True
    else:
        return False


# consonant_split
def c_spl(c_sect):
    '''returns cons of preceding and succeeding syllables, split by a '
    works only for blocks for supported cons symbols.'''
    c = re.search(c_re, c_sect)
    if c:
        return "'".join(c.groups())
    else:
        print(c_sect)
        print('Invalid/unsupported cons in cons block. C unsplittable')
        return


def vc_spl(sect):
    '''returns dict of leftmost vowel and consonant blocks, keys
    "v" and "c". Works for multi syll ONLY, with vow blocks at the ends'''
    vc = re.search(vc_re, sect)
    if vc:
        return vc.groupdict()
    else:
        print('sect: ' + sect)
        print('Invalid characters in the middle of the word. VC unsplittable')
        return


def blocks(sect):
    '''returns a list of the vowel and consonant blocks of a section
    works for mono/multi syll sections.'''
    bl = re.findall(anyblocks_re, sect)
    if len(''.join(bl)) == len(sect):
        return bl
    else:
        # print(sect)
        print('Invalid/unsupported characters somewhere. Unblockifiable.')
        return


def cut(word):
    '''returns dict of front(f), middle(m), back(b) part of the word, the
    ends being the cons blocks at the ends, works for mono/multi syll.'''
    ends = re.search(ends_re, word)
    if ends:
        return ends.groupdict()
    else:
        #print('hey: ' + word)
        print('Invalid characters at the ends of the word. Uncuttable')
        return


def syllable_separated(word):
    '''separates the syllables of a word in (supported) IPA characters

    cut cons blocks at the ends, so word starts and ends with vowel blocks
    block count will always be odd, and vowel blocks will always be at
    even indices 0,2,4,... In the case of monosyllable words, it is
    returned as is. Splits only happen at consonant blocks.
    '''
    # do not modify if word is a standalone symbol
    if is_symbol(word) == True:
        return word

    else:
        without_marks = cut_m(word)['m']
        mid = cut(without_marks)['m']
        mid_bl = blocks(mid)
        v_mid_bl = [v for v in mid_bl if mid_bl.index(v)%2 == 0]

        # for monosyllable words, no splitting required
        if len(v_mid_bl) <= 1:
            return cut_m(word)['f'] + cut(word)['f'] + mid +\
                     cut(word)['b'] + cut_m(word)['b']

        # or multisyllable words
        elif len(v_mid_bl) > 1:

            spl_w =''
            for _ in range(len(v_mid_bl)-1):

                # split v & c, apply ', then add to split_word
                # print(mid,'newmid')
                # print(vc_spl(mid)['c'],'cons of current vc')
                spl_c_bl = c_spl(vc_spl(mid)['c'])
                # print(spl_c_bl,'split c block')
                spl_vc = vc_spl(mid)['v'] + spl_c_bl
                # print(spl_vc,'split vc')
                spl_w = spl_w + spl_vc
                # print(spl_w,'spl_w')

                # remove what was syll'd from the mid block,
                # otherwise the conversion will not progress
                uspl_vc = (spl_vc.replace("'",''))
                # print(uspl_vc,'unsplit vc')
                # print(mid,'oldmid')
                # IMPORTANT: 1 means that only a maximum of 1 matches in the string
                # will be replaced. So the only the leftmost match.
                mid = mid.replace(uspl_vc, '', 1)

            # first cons bl + split mid bl + last vow bl + last cons bl
            return cut_m(word)['f'] + cut(word)['f'] + \
                    spl_w + mid + cut(word)['b'] + cut_m(word)['b']

