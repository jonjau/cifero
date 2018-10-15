# June 2018
# Overhauled October 2018

# Jonathan J

'''
cifero.translit

transliterate() and raw_transliterate() are the main functions here.

transliterate() converts sentences from one mode to another, optionally with
syllable separation and custom word separators. In the case that one of those
modes are English, a dictionary lookup is involved.

raw_transliterate is like transliterate except it undoes the syllable separation
and custom word separators.
'''

import re

import cifero.cmudict as cmudict
import cifero.sheets as sheets

from cifero.syll import syllable_separated


cipher_cons_bases = list(
    set([x[0] for x in sheets.sheetsdict['Cipher']['consonants'] if len(x)>0]))
cipher_vow_bases = list(
    set([x[0] for x in sheets.sheetsdict['Cipher']['vowels'] if len(x)>0]))
cipher_modifiers = list(
    set([x[1] if len(x)>1 else '' for x in sheets.sheetsdict['Cipher']['consonants']]))


def convert(query, from_mode, to_mode):
    '''Main conversion function, takes single character. Note that it doesn't
    raise an error if the query is not found.'''

    from_sheet = sheets.sheetsdict[from_mode]
    to_sheet = sheets.sheetsdict[to_mode]

    # consonants
    if query in from_sheet['consonants']:
        return to_sheet['consonants'][from_sheet['consonants'].index(query)]
    # vowels
    elif query in from_sheet['vowels']:
        return to_sheet['vowels'][from_sheet['vowels'].index(query)]
    # other
    else:
        return query


def standardize_cipher(word):
    '''Turns default Cipher word to IPA. Syllable separation and invalid chars
    stay as is. Also works for sentences.'''

    #each of these regexes have a negative lookbehind for the @ sign
    #doty'(?<!) and each re.sub() leaves a dot in front of the changed
    #char. This is to prevent the multiple re.sub() 's from overlapping
    #each other; each cipher character(s) is modified only once.

    #matches modified cipher vowels (modified vowels)
    vow_re = re.compile(r'''(?<!`)({0})[{1}]'''.format(
                        '|'.join(cipher_vow_bases),
                        ''.join(cipher_modifiers)), re.X)

    #matches non-modified cipher cons
    no_re = re.compile(r'''(?<!`)([{0}{1}])(?![{2}])'''.format(
                    ''.join(cipher_cons_bases),''.join(cipher_vow_bases),
                    ''.join(cipher_modifiers)), re.X)

    #matches f-modified cipher cons
    f_re = re.compile(r'''(?<!`)([{0}]{1})'''.format(
                        ''.join(cipher_cons_bases),
                        cipher_modifiers[1]), re.X)

    #matches n-modified cipher cons
    n_re = re.compile(r'''(?<!`)([{0}]{1})'''.format(
                        ''.join(cipher_cons_bases),
                        cipher_modifiers[2]), re.X)

    #replaces cipher with ipa equivalent from tabula
    word = re.sub(n_re, lambda c: '`'  + convert(c.group(),'Cipher','IPA'),word)
    word = re.sub(f_re, lambda c: '`'  + convert(c.group(),'Cipher','IPA'),word)
    word = re.sub(vow_re, lambda c: '`'+ convert(c.group(),'Cipher','IPA'),word)
    word = re.sub(no_re, lambda c: '`' + convert(c.group(),'Cipher','IPA'),word)
    word = re.sub(r'`', '', word)

    return word


def standardize_base(word):
    '''Turns Base word to IPA. Syllable separation and invalid chars stay as is.
    Also works for sentences. Only concerned with (...)'''

    #matches symbol combinations in brackets
    b_re = re.compile(r'\((.+?)\)')

    #matches single symbols without @ in front
    o_re = re.compile(r'(?<!`)\w')

    #replaces (...) with @...
    word = re.sub(b_re, lambda c: '`' + convert(c.group(), 'Base', 'IPA'), word)
    #replaces the other symbols
    word = re.sub(o_re, lambda c: convert(c.group(), 'Base', 'IPA'), word)

    word = re.sub(r'`', '', word)

    return word


def standardize_key(word):
    '''turns Key word to IPA. Syllable separation and invalid chars stay as is.
    No regex in the implementation, perfect one-to-one correspondence.'''
    new_word = ''
    for letter in word:
        new_word = new_word + convert(letter.lower(), 'Key', 'IPA')

    return new_word


# mc = mode_constant
def standardize(word, from_mode):
    '''turns word from ipa/key/cipher/english/etc to ipa, and separates
     its syllables with SINGLE QUOTES'''

    if from_mode == 'IPA':
        new_word = word.lower()

    elif from_mode == 'Base':
        new_word = standardize_base(word)
    
    elif from_mode == 'Key':
        new_word = standardize_key(word)

    elif from_mode == 'Cipher':
        new_word = standardize_cipher(word)

    #from plain english, raises errors very easily
    elif from_mode == 'English':
        # replace marks that are attached to the word, before looking it up in
        # the dict. syll() can handle standalone symbols
        lookup_query = word
        for letter in word:
            if letter in sheets.marks:
                lookup_query = word.replace(letter,'')
        lookup_result = cmudict.lookup_dict(lookup_query.lower())
        new_word = word.replace(lookup_query,lookup_result)

    return syllable_separated(new_word)


def translit_w(word, to_mode):
    '''converts IPA word to to_mc word. Syllables remain intact.'''
    new_word = []
    for letter in word:
        new_word.append(convert(letter,'IPA', to_mode))

    return new_word


def transliterate(sentence, from_mode, to_mode, syll_sep="'", word_sep=" "):
    '''Converts IPA/Key/Cipher/English sentence (with words separated by
    word_sep and syllables optionally separated by syll_sep) into
    IPA/Key/Cipher/English, with syllables separated by syll_sep and words
    separated by word_sep*. Transliterating from and to English involves a
    dictionary lookup, which can easily fail.
    
    *Make sure syll_sep and word_sep are unique strings not found as substrings
    in the sentence (in both modes).
    '''
    
    # convert syll_sep and word_sep to defaults
    # THIS CAN mess up the actual sentence, so make sure separators are unique

    if syll_sep != "'" or word_sep != " ":
        sentence = sentence.replace(syll_sep, "'")
        sentence = sentence.replace(word_sep, " ")

    ipa_sent = []
    for word in sentence.split():
        word = word.replace("'",'')
        ipa_sent.append(standardize(word, from_mode))

    new_sent = []
    if to_mode in sheets.sheetsdict.keys():
        for ipa_word in ipa_sent:
            new_sent.append(''.join(translit_w(ipa_word, to_mode)))

    #to plain english, extremely unreliable
    elif to_mode == 'English':
        for ipa_word in ipa_sent:
            new_sent.append(cmudict.reverse_lookup_dict(ipa_word))

    sentence = word_sep.join(new_sent)

    if syll_sep != "'":
        sentence = sentence.replace("'", syll_sep)

    return sentence


def raw_transliterate(sentence, from_mode, to_mode, syll_sep="'", word_sep=" "):
    '''Exactly like transliterate(), but does not apply/reapply the syllable
    /word separators to the output. This removes all occurences of syll_sep and 
    all word_sep's become spaces.'''

    sentence = transliterate(
        sentence, from_mode, to_mode, syll_sep=syll_sep, word_sep=word_sep)

    sentence = sentence.replace(syll_sep, '')
    sentence = sentence.replace(word_sep, ' ')

    return sentence


def strip_marks_and_symbols(word):
    '''removes marks :;,.!?[](){}"'<> and symbols *+-/~_
    &#$%@= are not replaced because they are used in default Key.
    ` is also left as is, for escaping purposes'''
    m_and_s_re = re.compile(r'''[:;,.!?[\](){}\"'<>*+-/~^_|\\]''')

    word = re.sub(m_and_s_re, '', word)

    return word


if __name__ == '__main__':
    import time
    start = time.time()
    for i in range(100000):
        convert('bf','Cipher','Base')
    print(time.time() - start)