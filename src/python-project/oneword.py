from bs4 import BeautifulSoup
import urllib.request

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
        self.names = []
        self.wordType = "Unknown"   # 
        self.pronunciations=[]      # Array of pronunciations; (One-element contains Pronounce and Link)
        self.meaning_by_wordtype = []   # Array of (Array of Meaning notes) = MeaningLine
        self.origin = ""                # History
        self.alternatives = []          # Array of OneWord (Alternative meanings/or wordtype)

        self.encoding = "UTF-8"

        

        return




class ScrapOneWord:
    def ScrapOneWord(self):
        return

def scrape_oneword(wordurl):
    fr = urllib.request.urlopen(wordurl)
    html = fr.read()
    fr.close()

    soup = BeautifulSoup(html)

    divMain = soup.find("div", "entryWrapper")

    wns = divMain.find_all("span", "hw")   # Word names
    aus = divMain.find_all("audio")        # Audio

    divMain.find_all("div", "primary_homograph")    # Alternative words


    wordtypes = divMain.find_all("span", "pos")
    gramms = divMain.find_all("section", "gramb")
    sembs = divMain.find_all("ul", "semb")

    myWord = OneWord()

    for wn in wns:
        # print(wn.text)
        myWord.names.append(wn.text)
    
    for au in aus:
        print(au)

    for wt in wordtypes:
        print(wt)
    
    print("There are grammars ", len(gramms))
    print("There are sembs ", len(sembs))

    for semb in sembs:
        print(semb.text)

    # Tổ chức 

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



"""
Cấu trúc từ:
    div(class=entryWrapper): chứa tất cả nội dung; bao gồm:
        (i) Tên (name)
        (ii) Tất cả pronounciations:
                Mỗi pronounce gồm:
                    Cách viết (phiên âm quốc tế)
                    URL tới MP3
        (iii) 


    HTML ở phía dưới bao gồm:
        tag header: chứa nội dung cơ sở, bao gồm: tên; pronounciation; 


    HTMLView:
        div<class=entryWrapper>
            Nhiều <div class="entryHead primary_homograph">
                Một <header>: chứa thông tin cơ sở về một alternative của từ () 
                    Có <h2 class="hwg"/>: có thông tin về từ.
                        <h3 class="pronounciations">
                            <span class="phoneticspelling">: Nội dung phát âm - pronounciation
                            <audio src="">: chứa link mp3 của phát âm.
        
            Nhiều <section class="gramb">:
                Có một <h3 class=ps pos>
                            <span class="pos">{loại_từ}</span>
                            <span class="pos-inflections">{dạng_của_loại_từ}</span>
                        </h3>
            
                có một <ul class="semb">
                    Có nhiều <li> - mỗi li này có 1 nghĩa lớn. Trong li thì:
                        <div class=trg>:
                            <p> đầu tiên có: 
                                Có <span class=iteration>: trong nội dung có chỉ mục (index) của nghĩa lớn.
                                Có <span class="grammatical_note">: chứa nội dung ghi chú ngữ pháp 
                                Có <span class="ind">: Chứa nội dung nghĩa lớn.

                                Có <div class="examples"/>: chứa các ví dụ
                                Có <ol class="subSenses"/>: chứa các dòng-nghĩa-chi tiết:
                                    Có nhiều <li class="subSense"/>: mỗi li này có đủ thông tin về dòng-nghĩa chi tiết.
                                        <span class="subsenseIteration">: chứa chỉ mục dòng-nghĩa-chi-tiết.
                                        <span class="ind">: nghĩa.
                                        <div class="exg">: Một ví dụ 
                                        <div class="examples">: các ví dụ 
                                        <div class="synonyms">: các thứ đồng nghĩa.
"""


