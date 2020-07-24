import string
import pycountry
import csv
import functools
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import codecs

class CoronaRelatedTech:
    def __init__(self,paper_name,paper_country,search_keyword_path,language):
        self.GeneratingCountryNames()
        self.GettingSearchKeyWords(search_keyword_path)
        self.language=language
        self.paper_name=paper_name
        self.paper_country=paper_country
        if(os.path.isfile('Extracted-Corona-Related-News-Articles.csv')):
            self.WRITE_FILE=open('Extracted-Corona-Related-News-Articles.csv','a',encoding="utf-8")
        else:
            self.WRITE_FILE=open('Extracted-Corona-Related-News-Articles.csv','a',encoding="utf-8")
            self.WRITE_FILE.write('date,categories,paper,paper_country,mentioned_countries,headline,summary,news,link\n')


    def GeneratingCountryNames(self):
        ################## Generating the country names ######################3
        list=pycountry.countries
        self.country_list=[]
        for i in list:
            self.country_list.append(i.name.lower())

    def GettingSearchKeyWords(self,path):
        ################# Getting the keywords ############################
        self.word_tag_map={}
        with open(path,'r',encoding="utf-8") as file:
            lines=file.readlines()
            for i in range(1,len(lines)):
                try:
                    l=lines[i].strip().split(',')
                    word=l[0].lower().strip()
                    word=self.RemovePunctuation(word)
                    category=l[1].lower().strip()
                    category=self.RemovePunctuation(category)
                    self.word_tag_map[word]=category
                except Exception as e:
                    print(e, " in keyword file.")
                    pass

    def RemovePunctuation(self,text):
        #Removing punctuation
        result = ""
        for i in text:
            if(i in string.punctuation):
                result = result + " "
            else:
                result = result+i
        return result

    def Tokenize(self,text):
        text = text.lower()
        result = text.split(" ")
        return result

    def RemoveStopwords(self, text):
        try:
            words = [w for w in text if w not in stopwords.words(self.language)]
        except Exception as e:
            print(e, " in learning stopwords.")
            words = [w for w in text if w not in stopwords.words('english')]
        return words

    def Lemmatize(self, text):
        lemmatizer = WordNetLemmatizer()
        lem_text = [lemmatizer.lemmatize(i) for i in text]
        return lem_text

    def CoronaValidation(self, text):
        if(self.language == 'english' or self.language == 'portuguese'):
            special_words = ['corona','coronavirus','corona virus','covid','covid19','covid-19','pandemic','epidemic','virus'] #virus
        else:
            special_words=[]
        for i in special_words:
            if(i in text):
                return True
        return False

    def SearchingCountryNames(self, text):
        found_countries=[]
        text = " ".join([i for i in text])
        for i in self.country_list:
            if(i in text):
                found_countries.append(i)
        return found_countries

    def Compare(self,list1,list2):
        if(list1[1]>list2[1]):
            return -1
        if(list1[1<list2[1]]):
            return 1
        return 0

    def FindingCategory(self,text):
        word_tag_map = self.word_tag_map
        dict={}
        for i in word_tag_map:
            search_text = i.split(' ')
            tag = word_tag_map[i]
            for j in range(0,len(text)):
                if(text[j] == search_text[0]):
                    flag=True
                    for k in range(0,len(search_text)):
                        if((j+k)<len(text) and search_text[k]==text[j+k]):
                            continue
                        else:
                            flag=False
                            break
                    if(flag==True):
                        if(word_tag_map[i] not in dict):
                            dict[word_tag_map[i]]=0
                        dict[word_tag_map[i]]=dict[word_tag_map[i]]+1
        list=[]
        for i in dict:
            list.append([i,dict[i]])
        list=sorted(list,key=functools.cmp_to_key(self.Compare))
        save=[]
        for i in range(0,min(2,len(list))):
            save.append(list[i][0])
        return save

    def WriteIntoFile(self,date,sorted_tags,paper,paper_country,mentioned_countries,headline,summary,news,link):
        self.WRITE_FILE.write(date+','+sorted_tags+','+paper+','+paper_country+','+mentioned_countries+','+headline+','+summary+','+news+','+link+"\n")
        return

    def ConcatenatList(self,list):
        result= ""
        for i in list:
            if(i==""):
                continue
            if(result == ""):
                result = i
            else:
                result = result + ';' + i
        return result

    def ProcessText(self,text):
        processed_text = self.RemovePunctuation(text)
        processed_text = self.Tokenize(processed_text)
        processed_text = self.RemoveStopwords(processed_text)
        return processed_text

    def GettingTheMentionedCountriesList(self,processed_headline,processed_summary,processed_news):
        countries=[]
        found_countries = self.SearchingCountryNames(processed_headline)
        found_countries = found_countries + self.SearchingCountryNames(processed_summary)
        found_countries = found_countries +  self.SearchingCountryNames(processed_news)
        for j in found_countries:
            if(j not in countries):
                countries.append(j)
        return countries

    def GettingTheTagsOfArticles(self,processed_headline,processed_summary,processed_news):
        tags = self.FindingCategory(processed_headline)
        tags = tags + self.FindingCategory(processed_summary)
        tags = tags + self.FindingCategory(processed_news)
        f_tags=[]
        for j in tags:
            if j not in f_tags:
                f_tags.append(j)
        return f_tags

    def Process(self,date,headline,summary,news,news_url):
        sp_char=['\n',',']
        headline = headline.strip()
        summary = summary.strip()
        news = news.strip()
        for i in range(0,len(sp_char)):
            headline=headline.replace(sp_char[i]," ")
            summary=summary.replace(sp_char[i]," ")
            news=news.replace(sp_char[i]," ")

        processed_headline = self.ProcessText(headline)
        processed_summary = self.ProcessText(summary)
        processed_news = self.ProcessText(news)

        f_tags = self.GettingTheTagsOfArticles(processed_headline,processed_summary,processed_news)
        if(len(f_tags)>0):
            print("CORONA RELATED NEWS FOUND")
            sorted_tags = self.ConcatenatList(f_tags)
            countries = self.GettingTheMentionedCountriesList(processed_headline,processed_summary,processed_news)
            mentioned_countries = self.ConcatenatList(countries)
            self.WriteIntoFile(date,sorted_tags,self.paper_name,self.paper_country,mentioned_countries,headline,summary,news,news_url)
