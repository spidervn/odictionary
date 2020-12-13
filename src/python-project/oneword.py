from bs4 import BeautifulSoup
from pathlib import Path
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

RET_SUCCESS = 0
RET_GENERAL_ERROR = 1
RET_TAG_NOTDEFINED = 2

ERR_CODE_GENERAL = 1
ERR_CODE_PARSE_TAG_NOTDEFINED = 2
ERR_CODE_PARSE_TAG_DATA_UNTRUE = 3


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

# scrape_oneword("https://www.lexico.com/definition/he")

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
                Và có các loại Section (đã biết) như sau:
                    (S-Meaning) Với loại section dạng <section class="gramb">; gọi là section-ý nghĩa; cấu trúc như sau
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
                    
                    (S-Etymology) Với loại Section dạng này (Dạng HTML: <section>, class chứa etymology) cấu trúc như sau:
                        Các Tag H3 là chứa Etymology-Item  (<h3 class="phrase-title">)
                        div class=senseInnerWrapper; chứa:
                            <ul class="semb gramb"> chứa các thành phần sau:
                                (tp01) các <strong class="phrase">: chứa nội dung từ.
                                (tp02) (tùy chọn - có hoặc không) (số lượng >= 0) <span> ([optional] class=sense-registers): nội dung giải nghĩa 
                                (tp03) <ul class="semb">: trong này có 
                                    <li> - trong này có:
                                        <div class="trg">
                                            <span class=iteration>
                                            <span class=grammatical_note>
                                            <span class=ind>: nội dung nghĩa
                                            <div class=examples>

                                            (Có thể có) <ol class=subSenses>: trong này có 
                                                <li class=subSense>
                                                    <span class="subsenseIteration">
                                                    <span class="form-groups">
                                                    <span class=ind>: Nội dung subsense
                                                    <div class=examples>: nội dung examples 

                Với section chưa biết thì gán nhãn vào loại Uncovered:
"""

def arr_contains(arr, e):
    for e1 in arr:
        if e1 == e:
            return True
    return False

def concat_2ndarray_to_first(arr1, arr2):

    if arr1 is None:
        return -1
    else:
        for a2 in arr2:
            arr1.append(a2)

    return 0
 
def grammar_section_meaning(sectionTag):
    sectionInfo = {}
    return

def grammar_section_etymology(sectionTag):
    sectionInfo = {}
    return


def grammar_section_undefined(sectionTag):

    return

def saveOneWord(wordurl):

    fr = urllib.request.urlopen(wordurl)
    html = fr.read()
    fr.close()

    soup = BeautifulSoup(html)
    divMain = soup.find("div", "entryWrapper")

    wordAlters = divMain.find_all("div", {'class': [ 'entryHead', 'primary_homograph']})
    sections = divMain.find("section")

    wordds = {} # Datastructure of this word
    wordds["alternatives"] = []
    audioURLs = []

    for i in range(len(wordAlters)):
        aHeader = wordAlters[i].find("header")
        alterName = aHeader.find("h2", "hwg") # Name of Alternatives 
        alterSpelling = aHeader.find("span", "phoneticspelling") # Spelling
        alterMp3 = aHeader.find("audio")

        # 
        # alterName.text
        # alterSpelling.text
        # alterMp3["src"]
        # 
        wordds["alternatives"].append({
            'name': alterName.text,
            'spelling': alterSpelling.text,
            'mp3': alterMp3["src"]
        })
        audioURLs.append(alterMp3["src"])

    # Every grammar
    for i in range(len(sections)):

        if arr_contains(sections[i]["class"], "gramb"):
            sectionData = grammar_section_meaning(sections[i])

        elif arr_contains(sections[i]["class"], "etymology"):
            

            # Move to section parsing
            wordType = sections[i].find("span", "pos")
            wordForms = sections[i].find("span", "pos-inflections")

            meaning_Ul = sections[i].find("ul", "semb")
            meaningUl_Lis = meaning_Ul.find_all("li")

            for j in range(len(meaningUl_Lis)):
                divTrg = meaningUl_Lis[j].find("div", "trg")

                spanIndex = divTrg.find("span", "iteration")
                spanGrammarNotes = divTrg.find("span", "grammatical_note")
                spanMean = divTrg.find("span", "ind")

                divExamples = divTrg.find("div", "examples")
                ol_subSense = divTrg.find("ol", "subSenses")

                liSubsenses = ol_subSense.find_all("li", "subSense")

                for k in range(len(liSubsenses)):
                    subSense = liSubsenses[k]
                    
                    subSenseIdx = subSense.find("span", "subsenseIteration")
                    subSenseTxt = subSense.find("span", "ind")
                    subSenseExample01 = subSense.find("span", "exg")

                    subSenseExamples = subSense.find("div", "examples")
                    subSenseSynonyms = subSense.find("div", "synonyms")


    # Alternatives


def parse_DivTrg(tagDiv):
    
    #
    # Tìm các tag bậc 1
    #   (i) Nếu là ol, có class=subSenses thì 
    #   (ii)
    # 

    #
    # Đầu ra là:
    #   Một dictionary 
    #   Hoặc là một Node mới trên Dictionary sẵn có.
    # 
    RET_SUCCESS = 0
    RET_GENERAL_ERROR = 1
    RET_TAG_NOTDEFINED = 2

    tags = tagDiv.find_all(recursive=False)

    ret = RET_SUCCESS
    arr_errors = []
    arr_problems = []   # Array of { problem_code: ; problem_source }

    ret_data = {}
    ret_data['notes'] = []              # Every notes: Grammar; History; Usage;
    ret_data['content'] = ''            # Meaning of Content   
    ret_data['direct_examples'] = []    # Direct Example Here
    ret_data['more_examples'] = []      # More Here
    ret_data['sub_senses'] = []         # List of detail meaning here
    
    for i in range(len(tags)):
        if tags[i].name == "ol":
            # 
            # TODO
            # arr_contains(tags[i]["class"], "subSenses"):
            # Parse subsense here
            # 
            lis = tags[i].find_all("li", "subSense", recursive=False)

            if len(lis) > 0:
                for j in range(len(lis)):
                    oneMeaningCollect = { }
                    oneMeaningCollect["direct_examples"] = []

                    spanIter = lis[j].find("span", "subsenseIteration")
                    spanContent = lis[j].find("span", "ind")
                    divDirectExamples = lis[j].find_all("div", "exg", recursive=False)
                    divMoreExamples = lis[j].find("div", "examples")
                                      
                    if not spanContent:
                        # Errror 
                        arr_problems.append({
                            'code': ERR_CODE_PARSE_TAG_NOTDEFINED,
                            'source': "",
                            'description': "Tag ol inside <div class=trg> has no Li?"
                        })
                    else:
                        oneMeaningCollect['content'] = spanContent.text

                    if spanIter:
                        oneMeaningCollect['iteration'] = spanIter.text

                    if divDirectExamples:
                        for ddE01 in divDirectExamples:
                            for ddE01_ConcreteEx in ddE01.find_all("div", "ex"):
                                oneMeaningCollect["direct_examples"].append(ddE01_ConcreteEx.text)
                    
                    if divMoreExamples:
                        liExs = divMoreExamples.find_all("li", "ex")

                        if liExs is not None and len(liExs) > 0:
                            for liEx01 in liExs:
                                oneMeaningCollect["more_examples"].append(liEx01.text)
                        else:
                            # Errror 
                            arr_problems.append({
                                'code': ERR_CODE_PARSE_TAG_NOTDEFINED,
                                'source': "",
                                'description': "Tag ol inside <div class=trg> has no Li?"
                            })
            else:
                arr_problems.append({
                    'code': ERR_CODE_PARSE_TAG_NOTDEFINED,
                    'source': "",
                    'description': "Tag ol inside <div class=trg> has no Li?"
                })
        elif tags[i].name == "div":
            # Direct Example
            if arr_contains(tags[i]["class"], "exg"):
                for tag_directExample in tags[i].find_all("div", "ex"):
                    ret_data['direct_examples'].append(tag_directExample.text)

            elif arr_contains(tags[i]["class"], "examples"):
                for tag_ex in tags[i].find_all("li", "ex"):
                    ret_data['more_examples'].append(tag_ex.text)
            else:
                arr_problems.append({
                    'code': ERR_CODE_PARSE_TAG_NOTDEFINED,
                    'source': "",
                    'description': "div Tag inside <div=trg> uncovered"
                })

        # Text processing
        else:
            # Gather all text here
            # Find Every tags 
            # Get All-text here 

            stack = [tags[i]]

            _spans =  tags[i].find_all("span")
            _strongs =  tags[i].find_all("strong")
            _h2s =  tags[i].find_all("h2")
            _h3s =  tags[i].find_all("h3")
            _h4s =  tags[i].find_all("h4")

            if tags[i].name == 'span' or tags[i].name == 'strong' or tags[i].name == 'h2' or tags[i].name == 'h3' or tags[i].name == 'h4':
                ret_data['notes'].append(tags[i].text)

            for span in tags[i].find_all("span"):
                ret_data['notes'].append(span.text)
            for strong in tags[i].find_all("strong"):
                ret_data['notes'].append(strong.text)
            for h2 in tags[i].find_all("h2"):
                ret_data['notes'].append(h2.text)
            for h3 in tags[i].find_all("h3"):
                ret_data['notes'].append(h3.text)
            for h4 in tags[i].find_all("h4"):
                ret_data['notes'].append(h4.text)
        
    return [{ 'error_list': arr_problems }, ret_data]

def parse_section_meaning(tagSection):

    spans = tagSection.find_all("span", recursive=False)

    info = []
    primary_idx = 0

    section_data = {
        'title': [],
        'notes': [],
        'content': '', # Main content 
        # TODO
        # 'meaning_iter': []
    }

    for i in range(len(spans)):
        info.append(spans[i].text)
        
        if arr_contains(spans[i]["class"], "pos"):
            primary_idx = i


    uls = tagSection.find_all("ul", "semb")
    for i in range(len(uls)):
        lis = uls[i].find_all("li")

        for j in range(len(lis)):
            divTrg = lis[j].find("div", "trg", recursive=False)

    # return {
    #     'title': len(info) > 0 ? info[primary_idx] : "",
    #     'info': info
    # }
    return None

def parse_section(tagSection):
    
    """
        Parse Section Type
    """
    SECTION_TYPE_UNCOVERED = -1
    SECTION_TYPE_GRAMMAR_MEANING = 1
    SECTION_TYPE_ETYMOLOGY = 2
    sectionType = -1

    error_list = []

    section_data = None
    ret = {}

    if arr_contains(tagSection["class"], "gramb"):
        sectionType = SECTION_TYPE_GRAMMAR_MEANING
    elif arr_contains(tagSection["class"], "etymology"):
        sectionType = SECTION_TYPE_ETYMOLOGY

    if sectionType == SECTION_TYPE_GRAMMAR_MEANING:
        ret, section_data =  parse_section_meaning(tagSection)
    elif sectionType == SECTION_TYPE_ETYMOLOGY:
        ret, section_data = parse_section_etymology(tagSection)
    else:
        # Exception HERE
        # Store all HTML
        error_list.append({
            'code': ERR_CODE_GENERAL,
            'source': "",
            'description': "Uncovered sections"
        })

    concat_2ndarray_to_first(error_list, ret['error_list'])
    return [ { 'error_list': error_list}, section_data ]

def example_of_datastructure():
    aa = {}
    aa["name"] = "grammar"
    aa["spelling"] = "/grammar/"
    aa["info"] = {
        'Guest': 11,
        'Room': "Room0003"
    }
    aa['networks'] = []
    aa['networks'].append(2)
    aa['networks'].appparse_section

class RunConfiguration:
    def __init__(self):
        self.BaseOutputFolder = ""
        self.EachWordAudioFolder = ""
        return

class LexicoGrabber:
    def __init__(self, config):
        self.config = config
        return

    def is_in_local_db(self, word):
        filecheck_01 = Path(config.BaseOutputFolder + "/" + word + "/" + word + ".json")
        filecheck_02 = Path(config.BaseOutputFolder + "/" + word + "/" + word + ".html")
        filecheck_02 = Path(config.BaseOutputFolder + "/" + word + "/" + config.EachWordAudioFolder + "/")

        return

    def run_sync_one_word(self, word):
        return    



soup = BeautifulSoup(html)
divMain = soup.find("div", "entryWrapper")
sections = divMain.find_all("section")

print(len(sections))
for i in range(len(sections)):
    if arr_contains(sections[i]["class"], "gramb"):
        pass
    else:
        # General text
        print("----------------------")
        print("")
        print("----------------------")

# An example of a section 
section01 = {}
section01["titile"] = "Phrases"
section01["info"] = [ "Noun", "(Etyologies)", "[mass noun]" ]

tags = divMain.find_all(recursive=False)
print(len(tags))
print(tags[0].name)

divMain.find_all(recursive=False)

lexico_config = RunConfiguration()
lexico_config.BaseOutputFolder = "./lexico_dict"
lexico_config.EachWordAudioFolder = "audio"

