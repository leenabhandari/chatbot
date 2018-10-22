import pymysql
import spacy
from spacy.matcher import Matcher

connection = pymysql.connect(host='206.189.134.31',
                             user='intern',
                             password='****',
                             db='chatbot'
                            )

cursor=connection.cursor()
cursor.execute("show tables")
results=cursor.fetchall()
#print(results)
cursor.execute("select * from master_skill")
#print(cursor.fetchall())

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
