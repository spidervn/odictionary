from bs4 import BeautifulSoup
import urllib2
import enum

#
# Oneword to json
# 

WordType_Noun = 1
WordType_Verb = 2
WordType_Adjective = 3
WordType_Preposition = 4
WordType_Phrases = 5
WordType_Unknown = 6

class MeaningItem:
    self.meaning = ""
    self.extra_note = ""
    self.examples = []

    def MeaningItem(self):
        return

class MeaningNote:
    def MeaningNote(self):
        self.meaning = MeaningItem()
        self.child_meanings = []    # Array of meaning items
        return

class OneWord:
    self.name = ""              # 
    self.wordType = "Unknown"   # 
    self.pronunciations=[]      # Array of pronunciations

    self.meaning_by_wordtype = []   # Array of (Array of Meaning notes)
    self.origin = ""                # History
    self.alternatives = []          # Array of OneWord (Alternative meanings/or wordtype)
    
    def OneWord(self):
        return

    def OneWord(self):
        return

class ScrapOneWord:

    def ScrapOneWord(self):
        return

fr = urllib2.urlopen("https://en.oxforddictionaries.com/definition/odometry")
html = fr.read()
fr.close()

# page = requests.get("https://en.oxforddictionaries.com/definition/odometry")
soup = BeautifulSoup(html) # page.content, "html.parser")

print soup.title
print soup.p

a = soup.find(class="hwg")
for link in a:
    print "One: "
    print a

