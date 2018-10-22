import spacy
from textblob import TextBlob
print ("Hello there! I am Lee, your virtual assistant..")
name=input("What is your name?")
nlp=spacy.load('en')
doc=nlp(name)
for token in doc:
    print(token.text+" "+token.pos_)
'''
for word in doc:
    print(word)

for sent in doc.sents:
    print(sent.text)'''


for np in doc.noun_chunks:
    print(np)

document="This is a nice document"
blob=TextBlob(document)

print (blob.sentences)

for sent  in blob.sentences:
    print (sent.sentiment)
