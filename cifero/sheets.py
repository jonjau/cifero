# October 2018

'''
cifero.sheets

Modules syll and translit use cifero.sheets.sheetsdict in their functions.
'''

################################################################################
# default cipher sheets
# better not change these
# these aren't linked to the main program.

ipa_sheet = {
    'title': 'IPA',
    'consonants':
    [
    'p','b','',
    't','d','',
    'k','g','',
    'θ','ð','',
    'f','v','',
    's','z','ʦ',
    'ʃ','ʒ','',
    'ʧ','ʤ','',
    'h','x','ɲ',
    'n','m','ŋ',
    'l','ɹ','r',
    'ʔ','j','w'
    ],
    'vowels':
    [
    'ɑ','a','',
    'ɪ','i','',
    'ʊ','u','',
    'ɛ','e','',
    'o','ɔ','',
    'ə','ʌ','',
    'æ','',''
    ]
}

key_sheet = {
    'title' : 'Key',
    'consonants':
    [
    '9','b','',
    '1','d','',
    '7','g','',
    'f','t','',
    '8','v','',
    '0','z','c',
    'q','p','',
    '6','j','',
    'h','k','m',
    '2','3','n',
    '5','4','r',
    'l','y','w'
    ],
    'vowels':
    [
    'a','&','',
    'i','#','',
    'u','$','',
    'e','%','',
    'o','@','',
    'x','=','',
    's','',''
    ]
}

base_sheet = {
    'title' : 'Base',
    'consonants':
    [
    'p','b','',
    't','d','',
    'k','g','',
    '(th)','(dth)','',
    'f','v','',
    's','z','(ts)',
    '(sh)','(jh)','',
    '(ch)','j','',
    'h','(kh)','(ny)',
    'n','m','(ng)',
    'l','r','(rr)',
    '(-)','y','w'
    ],
    'vowels':
    [
    'a','(aa)','',
    'i','(ii)','',
    'u','(oo)','',
    'e','(ee)','',
    'o','(aw)','',
    '(uh)','(ah)','',
    '(ea)','',''
    ]
}

cipher_sheet = {
    'title' : 'Cipher',
    'consonants':
    [
    'b','bf','',
    'd','df','',
    'g','gf','',
    't','tf','',
    'p','pf','',
    'c','cf','cn',
    'k','kf','',
    'q','qf','',
    'h','hf','hn',
    'm','mf','mn',
    'r','rf','rn',
    'w','wf','wn'
    ],
    'vowels' :
    [
    'l','lf','',
    'j','jf','',
    'y','yf','',
    'z','zf','',
    'v','vf','',
    'x','xf','',
    's','',''
    ]
}

# note that 'marks' and 'symbols' are somewhat arbitrarily classified by their
# relative position in a word. This is strict and inputs often don't conform
# To be safe, just strip punctuation before transliterating.

# list of punctuation marks. These must be attached to the end of a word
# \ undefined
marks = (
':', ';', ',', '.', '!', '?',
'[', ']', '(', ')', '{', '}',
'"',"'",'<','>'
)
# list of symbols. These must stand alone in a sentence
# _ ^ | undefined
# Edit Oct '18: &#$%@= are now used for default key (capitalization problems)
symbols = (
'*','+','-','/','~'
)

def fl(list1):
    '''remove empty strings from list'''
    list1 = list(filter(None, list1))
    return list1

# cons in IPA, 'class t'
reg1_c   = fl(ipa_sheet['consonants'][:15] + ipa_sheet['consonants'][21:24])
# cons in IPA, 'class s'
reg2_c   = fl(ipa_sheet['consonants'][15:17] + ipa_sheet['consonants'][18:21])
# cons in IPA, 'class h'
irreg1_c = fl(ipa_sheet['consonants'][24:26])
# cons in IPA, 'class n'
irreg2_c = fl(ipa_sheet['consonants'][26:30])
# cons in IPA, 'class r'
irreg3_c = fl(ipa_sheet['consonants'][30:33])
# pseudo-vowels in IPA
pseudo_v = fl(ipa_sheet['consonants'][34:])
other_c  = fl([ipa_sheet['consonants'][17]] + [ipa_sheet['consonants'][33]])


def init_vcc():
    '''cons clusters by their "classes"'''
    vcc_st = [s + t for s in reg2_c for t in reg1_c]
    vcc_sn = [s + n for s in reg2_c for n in irreg2_c]
    vcc_sr = [s + r for s in reg2_c for r in irreg3_c]
    vcc_tr = [t + r for t in reg1_c for r in irreg3_c]

    return vcc_st + vcc_sn + vcc_sr + vcc_tr

# valid consonant clusters in IPA
vcc = init_vcc()


################################################################################

sheetsdict = {ipa_sheet['title'] : ipa_sheet,
              key_sheet['title']: key_sheet,
              base_sheet['title'] : base_sheet,
              cipher_sheet['title'] : cipher_sheet}

################################################################################