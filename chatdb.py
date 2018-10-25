import pymysql
import re
import spacy
from spacy.matcher import Matcher
from textblob import TextBlob



'''
for word in doc:
    print(word)

for sent in doc.sents:
    print(sent.text)'''

#
# for np in doc.noun_chunks:
#     print(np)
#
# document="This is a nice document"
# blob=TextBlob(document)
#
# print (blob.sentences)
#
# for sent  in blob.sentences:
#     print (sent.sentiment)


connection = pymysql.connect(host='206.189.134.31',
                             user='intern',
                             password='Change@Pass',
                             db='chatbot'
                            )

cursor=connection.cursor()
cursor.execute("show tables")
results=cursor.fetchall()
#print(results)
cursor.execute("select skill_nm from master_skill")
skills=cursor.fetchall()
#print(skills)
skills=[x[0] for x in skills]
print(skills)
#cursor.execute("select * from master_user")
#results=cursor.fetchall()
#print(results)

def get_pattern(term):
    pattern=list()
    for b in term.split():
        pattern.append({'LOWER':b.lower()})
    return pattern

def build_patterns(terms):
    patterns=[]
    for term in terms:
        patterns.append(get_pattern(term))
    return list(zip(terms,patterns))

class SpacyMatcher():
    def __init__(self,terms):
        self.__nlp__=spacy.load('en')
        self.matcher=Matcher(self.__nlp__.vocab)
        self.patterns=build_patterns(terms)
        self.built_matcher(self.patterns)

    def built_matcher(self,patterns):
        for pattern in patterns:
            self.matcher.add(pattern[0],None,pattern[1])


    def getEntities(self,text, submatch=False):
        entities=[]
        doc=self.__nlp__(text)
        matches=self.matcher(doc)
        verbs=self.getVerbs(doc)

        for b in matches:
            match_id,start,end=b
            entities.append(doc[start:end].text)

        if(submatch):
            return list(set(b for b in entities if b not in verbs))
        else:
            return self.cleanEntity(text,list(set(b for b in entities if b not in verbs)))


    def getVerbs(self,doc):
        verbs=[toks.text for toks in doc if toks.pos_ in['VERB','PRON'] and toks.text.upper()!=toks.text]
        return verbs

    def cleanEntity(self,text,entities):
        new_list=[]
        if(len(entities)<=0):
            return entities
        modeEntities=[(entity,len(entity)) for entity in entities]
        #print(modeEntities)
        modeEntities=sorted(modeEntities,key=lambda x:x[1])
        #print(modeEntities)
        if(modeEntities[0][1]==modeEntities[len(modeEntities)-1][1]):
            return entities

        for ix in range(len(modeEntities)):
            item1,length1=modeEntities[ix]
            #print (modeEntities)
            is_sub=False

            for yz in range(ix+1,len(modeEntities)):
                item2,length2=modeEntities[yz]

                if(length1==length2 or item1 not in item2):
                    continue

                p1=re.compile(r'\b{}\b'.format(item1))
                item1_indices=[mm.span() for mm in p1.finditer(text)]

                p2=re.compile(r'\b{}\b'.format(item2))
                item2_indices=[mm.span() for mm in p2.finditer(text)]

                if(len(item1_indices)<=len(item2_indices)):
                    is_sub=True

            if not is_sub:
                new_list.append(item1)
        return new_list


print ("Hello there! I am Lee, your virtual assistant..")
name=input("What is your name?")
nlp=spacy.load('en')
doc=nlp(name)
for token in doc:
   # print(type(token.pos_))
    #print(token.text+" "+token.pos_)
    if(token.pos_ in ['PROPN'] ):
        print("Hello "+str(token)+" Have a nice day")

#skills=["python","android","java","c++"]
pm=SpacyMatcher(skills)
job_desc=input("Enter the job description:")
#skill_in_text=re.sub("[^\w]"," ",job_desc).split()
skill_in_text=pm.getEntities(job_desc)
#skill_in_text=pm.getEntities("Jobs available for Branding, Auditing at ABC company at XYZ location")
for skill in list(skill_in_text):
    print ((skill))
