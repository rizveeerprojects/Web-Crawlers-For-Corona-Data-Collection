#Main goal is to extract information based on newspaper crawling
#To identify the fighting mechanism of each country

import nltk
#nltk.download()
import string
import pycountry
import csv
import functools

################## Generating the country names ######################3
list=pycountry.countries
country_list=[]
for i in list:
    country_list.append(i.name.lower())

################# Getting the keywords ############################
word_tag_map={}
with open('Keywords-zaber-sir.csv','r') as file:
    csv_lines = csv.DictReader(file)
    for row in csv_lines:
        word = row['Word'].strip().lower()
        category = row['Category'].strip().lower()
        word_tag_map[word]=category

from nltk.corpus import stopwords
#from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
#from nltk.stem.porter import PorterStemmer

file_urls =['E:/Research/Web-Crawlers-For-Corona-Data-Collection/Newspapers/Guardian/guardian_data_news_data.csv']
paper_country_list = ['UK']
paper_name_list = ['Guardian']

################## Resultant file ################3
try:
    WRITE_FILE = open('Extracted Information.csv','r')
    WRITE_FILE = open('Extracted Information.csv','a')
except Exception as e:
    WRITE_FILE = open('Extracted Information.csv','a')
    WRITE_FILE.write('date,sorted_tags,paper,paper_country,mentioned_countries,headline,summary,news,link\n')



def RemovePunctuation(text):
    result = ""
    for i in text:
        if(i in string.punctuation):
            result = result + " "
        else:
            result = result+i
    return result

def Tokenize(text):
    text = text.lower()
    result = text.split(" ")
    """
    tokenizer = RegexpTokenizer(' ')
    result = tokenizer.tokenize(text.lower())
    """
    return result

def RemoveStopwords(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words

def Lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    lem_text = [lemmatizer.lemmatize(i) for i in text]
    return lem_text

def CoronaValidation(text):
    special_words = ['corona','coronavirus','corona virus','virus','covid','covid19','covid-19','pandemic','epidemic']
    for i in special_words:
        if(i in text):
            return True
    return False

def SearchingCountryNames(text):
    global country_list
    found_countries=[]
    for i in country_list:
        if(i in text):
            found_countries.append(i)
    return found_countries

def Compare(list1,list2):
    if(list1[1]>list2[1]):
        return -1
    if(list1[1<list2[1]]):
        return 1
    return 0

def FindingCategory(text):
    global word_tag_map
    dict={}
    text = "".join([i for i in text])
    for i in word_tag_map:
        if(i in text and i != " "):
            if(word_tag_map[i] not in dict):
                dict[word_tag_map[i]]=0
            dict[word_tag_map[i]]=dict[word_tag_map[i]]+1

    list=[]
    for i in dict:
        list.append([i,dict[i]])
    list=sorted(list,key=functools.cmp_to_key(Compare))
    save=[]
    for i in range(0,min(2,len(list))):
        save.append(list[i][0])
    return save

def WriteIntoFile(date,sorted_tags,paper,paper_country,mentioned_countries,headline,summary,news,link):
    global WRITE_FILE
    WRITE_FILE.write(date+','+sorted_tags+','+paper+','+paper_country+','+mentioned_countries+','+headline+','+summary+','+news+','+link+"\n")
    return

def ConcatenatList(list):
    result= ""
    for i in list:
        if(i==""):
            continue
        if(result == ""):
            result = i
        else:
            result = result + ';' + i
    return result

def ReadFile(file_name,paper_country,paper_name):

    with open(file_name,'r') as file:
        lines=file.readlines()
        for i in range(0,len(lines)):
            line = lines[i].split(",")
            date = line[0]
            link = line[1]
            base_category = line[2]
            headline = line[3]
            summary = line[4]
            news = line[5]

            #clearing headline
            processed_headline = RemovePunctuation(headline)
            processed_headline = Tokenize(processed_headline)
            processed_headline = RemoveStopwords(processed_headline)

            #clearing summary
            processed_summary = RemovePunctuation(summary)
            processed_summary = Tokenize(processed_summary)
            processed_summary = RemoveStopwords(processed_summary)

            #clearing news
            processed_news = RemovePunctuation(news)
            processed_news = Tokenize(processed_news)
            processed_news = RemoveStopwords(processed_news)


            corona_validation = CoronaValidation(processed_news)
            if(CoronaValidation(processed_headline) == True or CoronaValidation(processed_summary) == True or  CoronaValidation(processed_news) == True):
                print("YES CORONA NEWS")
                countries=[]
                found_countries = SearchingCountryNames(processed_headline)
                found_countries = found_countries + SearchingCountryNames(processed_summary)
                found_countries = found_countries +  SearchingCountryNames(processed_news)
                for j in found_countries:
                    if(j not in countries):
                        countries.append(j)
                tags = FindingCategory(processed_headline)
                tags = tags + FindingCategory(processed_summary)
                tags = tags + FindingCategory(processed_news)
                f_tags=[]
                for j in tags:
                    if j not in f_tags:
                        f_tags.append(j)
                sorted_tags = ConcatenatList(f_tags)
                mentioned_countries = ConcatenatList(countries)
                news = " ".join([j for j in processed_summary])
                WriteIntoFile(date,sorted_tags,paper_name,paper_country,mentioned_countries,headline,summary,news,link)


def Initiate():
    global file_urls,paper_country_list,paper_name_list
    for i in range(0,len(file_urls)):
        ReadFile(file_urls[i],paper_country_list[i],paper_name_list[i])
Initiate()
