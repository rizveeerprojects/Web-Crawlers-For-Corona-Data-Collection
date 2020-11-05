from bs4 import BeautifulSoup
from requests import get
import datetime
import os, sys
import json, sys

class ProthomAlo:

    def __init__(self,starting_date,number_of_days):
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.prothomalo.com"
        self.file_ptr = open('Abuse-News-ProthomAlo.txt','w',encoding="utf-8")
        self.file_ptr.write('date,headline,url\n')

    def EnglishDateConversion(self,year,month,day):
        b_num = ['০','১','২','৩','৪','৫','৬','৭','৮','৯']
        year = year.strip()
        string = ""
        print("year = ",year,len(year))
        for i in range(0,len(year)):
            for j in range(0,len(b_num)):
                if(year[i]==b_num[j]):
                    string=string+str(j)

        year = string
        print(year)
        day = day.strip()
        string = ""
        for i in range(0,len(day)):
            for j in range(0,len(b_num)):
                if(day[i]==b_num[j]):
                    string = string + str(j)
        day = string
        month = month.strip()
        bangla_month = ['জানুয়ারী','ফেব্রুয়ারি','মার্চ','এপ্রিল','মে','জুন','জুলাই','অগাস্ট','সেপ্টেম্বর','অক্টোবর','নভেম্বর','ডিসেম্বর']
        for i in range(0,len(bangla_month)):
            if(bangla_month[i]==month):
                month = str(i+1)
                break
        return year, month, day

    def CrawlEachPage(self,link):
        url = link
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        #date
        try:
            d = html_soup.find('div',class_='storyPageMetaData-m__publish-time__19bdV')
            print(d)
            span = d.find('span')
            span = span.text
            span = span.split(':')[1].strip()
            span = span.split(',')[0].split(' ')
            year,month,day = span[2],span[1],span[0]
            year,month,day = self.EnglishDateConversion(year,month,day)
            print(year,month,day)
        except Exception as e:
            return False,False,False,False,False

        #headline
        try:
            headline = html_soup.find_all('h1')
            headline = headline[0].text.strip()
            #print(headline)
        except Exception as e:
            return False,''

        #news
        try:
            news = html_soup.find_all('p')
            text = ''
            for i in range(0,len(news)):
                text = text + " "+news[i].text
        except Exception as e:
            return headline,False
        #print(headline)
        #print(summary)
        print(len(text))
        return (year,month,day,headline,text)

    def NewsValidation(self,text):
        string = text.strip().split(' ')
        words = ['ধর্ষণ','ধর্ষণের','ধর্ষিত','ধর্ষণে','ধর্ষিতা','নির্যাতন','নির্যাতনের']
        for i in range(0,len(string)):
            for j in words:
                if(j in string[i]):
                    return True
        return False

    def ApiCall(self,year1,month1,day1,gap):
        limit = 100
        offset = 0
        last_date = datetime.datetime(int(year1),int(month1),int(day1)) - datetime.timedelta(days=gap)
        list_urls = []
        while True:
            url = 'https://www.prothomalo.com/api/v1/collections/bangladesh/?limit=100&offset='+str(offset)
            for i in range(0,10):
                response = get(url)
                if(response.status_code == 503):
                    return
                else:
                    print(response.status_code,type(response))
                    response = response.json()
                    break
            for key in response:
                if(key != 'items'):
                    continue
                for i in range(0,len(response[key])):
                    url = response[key][i]['story']['url']
                    headline = response[key][i]['item']['headline'][0]
                    print(url)
                    if(url in list_urls):
                        continue
                    year,month,day,headline,news = self.CrawlEachPage(url)
                    print(year,month,day)
                    if(year==False):
                        for j in range(0,5):
                            year,month,day,headline,news = self.CrawlEachPage(url)
                            if(year !=False):
                                break
                    if(year==False):
                        continue
                    d=datetime.datetime(int(year),int(month),int(day))
                    if(d<last_date):
                        return
                    if(headline != False and news != False):
                        verdict = self.NewsValidation(headline)
                        if(verdict == False):
                            verdict = self.NewsValidation(news)
                        if(verdict == True):
                            self.file_ptr.write(str(d)+','+headline+','+url+'\n')
                            list_urls.append(url)
            offset = offset + 100

prothom_alo = ProthomAlo("","")
prothom_alo.ApiCall(2020,10,7,60)
