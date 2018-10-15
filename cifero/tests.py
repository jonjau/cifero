import cifero.translit as tl

#import ..cifero.transliterate

# Simple tests for the four default sheets

tpi = 'ɑɹ ðoʊz ʃaɪ jʊɹeɪʒɪən fʊtwɛɹ, kaʊbɔɪ ʧæps ɔɹ ʤɑli əɹθmuvɪŋ hɛdgɪɹ?'
tpk = 'a4 touz q&i yu4%ipix2 8u1we4, 7&ub@i 6s90 @4 ja5# x4f3$vin hedgi4?'
tpc = 'lrf tfvycf kllj jnyrfzzjkfjxm pydynzrf, gllybfvvj qsbc vvrf qflrjj \
        xrftmfyypfjmn hzdfgfjrf?'
tpc = 'lrf tfvycf klfj wfyrfzfjkfjxm pydwnzrf, glfybfvfj qsbc vfrf qflrjf \
        xrftmfyfpfjmn hzdfgfjrf?'
tpe = 'are those shy eurasian footwear, cowboy chaps or jolly earthmoving headgear?'

test_sentences = {'IPA' : tpi,
                  'Key' : tpk,
                  'Cipher' : tpc,
                  'English' : tpe}

print(tl.transliterate(tpi, 'IPA', 'IPA'))
print(tl.transliterate(tpk, 'Key', 'IPA'))
print(tl.transliterate(tpc, 'Cipher', 'IPA'))
print(tl.transliterate(tpe, 'English', 'IPA'), '<Approx.>')

print(tl.transliterate(tpi, 'IPA', 'Key'))
print(tl.transliterate(tpk, 'Key', 'Key'))
print(tl.transliterate(tpc, 'Cipher', 'Key'))
print(tl.transliterate(tpe, 'English', 'Key'), '<Approx.>')

print(tl.transliterate(tpi, 'IPA', 'Cipher'))
print(tl.transliterate(tpk, 'Key', 'Cipher'))
print(tl.transliterate(tpc, 'Cipher', 'Cipher'))
print(tl.transliterate(tpe, 'English', 'Cipher'), '<Approx.>')

print(tl.transliterate(tpi, 'IPA', 'Base'))
print(tl.transliterate(tpk, 'Key', 'Base'))
print(tl.transliterate(tpc, 'Cipher', 'Base'))
print(tl.transliterate(tpe, 'English', 'Base'), '<Approx.>')
