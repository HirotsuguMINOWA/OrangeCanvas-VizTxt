from janome.tokenizer import Tokenizer, Token

t = Tokenizer()

s = 'すもももももももものうち'

print(type(t.tokenize(s)))
# <class 'generator'>

print(type(t.tokenize(s).__next__()))
# <class 'janome.tokenizer.Token'>

print(type(list(t.tokenize(s))))
print(list(t.tokenize(s)))

for token in t.tokenize(s):  # type: Token
    print(token.part_of_speech.split(','))
