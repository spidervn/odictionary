from bs4 import BeautifulSoup
import urllib2
from json import JSONEncoder
import json

#
# Oneword to json
# 

WordType_Noun = 1
WordType_Verb = 2
WordType_Adjective = 3
WordType_Preposition = 4
WordType_Phrases = 5
WordType_Unknown = 6

class MeaningItem(JSONEncoder):
    def __init__(self):
        self.meaning = ""
        self.extra_note = ""
        self.examples = []
        return

class MeaningNote(JSONEncoder):

    def __init__(self, name, age):
        self.meaning = MeaningItem()
        self.child_meanings = []    # Array of meaning items
        return

class OneWord(JSONEncoder):
    def __init__(self):
        self.name = ""              # 
        self.wordType = "Unknown"   # 
        self.pronunciations=[]      # Array of pronunciations
        self.meaning_by_wordtype = []   # Array of (Array of Meaning notes)
        self.origin = ""                # History
        self.alternatives = []          # Array of OneWord (Alternative meanings/or wordtype)

        self.encoding = "UTF-8"
        return

class ScrapOneWord:
    def ScrapOneWord(self):
        return

def scrape_oneword(wordurl):
    fr = urllib2.urlopen(wordurl)
    html = fr.read()
    fr.close()

    soup = BeautifulSoup(html)

    divMain = soup.find("div", "entryWrapper")

    wns = divMain.find_all("span", "hw")   # Word names
    aus = divMain.find_all("audio")        # Audio

    wordtypes = divMain.find_all("span", "pos")
    gramms = divMain.find_all("section", "gramb")
    sembs = divMain.find_all("ul", "semb")

    for wn in wns:
        print(wn)
    
    for au in aus:
        print(au)

    for wt in wordtypes:
        print(wt)
    
    print("There are grammars ", len(gramms))
    print("There are sembs ", len(sembs))

    for semb in sembs:
        print(semb.text)

    return

# wordurl = "https://www.lexico.com/definition/do"
# fr = urllib2.urlopen(wordurl)
# html = fr.read()
# fr.close()

# # page = requests.get("https://en.oxforddictionaries.com/definition/odometry")
# soup = BeautifulSoup(html) # page.content, "html.parser")

# print soup.title
# print soup.p

# a = soup.find(class="hwg")
# for link in a:
#     print "One: "
#     print a

w = OneWord()
w.name = "publicity"

s = json.dumps(w.__dict__)
print(s)

scrape_oneword("https://www.lexico.com/definition/he")

