from bs4 import BeautifulSoup
from requests import get
import datetime
import os, sys
import json, sys


global_try_parameter=20

class Publico:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.publico.pt/"

    def CrawlEachPage(self,link):
        url = link
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        #headline
        try:
            headline = html_soup.find_all('h1',class_='headline story__headline')
            headline = headline[0].text.strip()
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = html_soup.find('div',class_='story__blurb lead', attrs={'itemprop':'description'}).text.strip()
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = html_soup.find('div',class_='story__content',id='story-content')
            news = news.find_all('p')
            text = ''
            for i in range(0,len(news)):
                text = text + " "+news[i].text
        except Exception as e:
            return headline,summary,False
        return (headline,summary,text)

    def FetchAllLinks(self,link,date):
        url_list=[]
        global global_try_parameter
        for i in range(0,1000,1):
            url = link+'/?page='+str(i+1)
            ## DEBUG: print(url)
            response = get(url)
            response = response.json()
            if(len(response) == 0):
                break
            for j in range(0,len(response)):
                if(response[j]['url'] not in url_list):
                    url_list.append(response[j]['url'])
        for i in range(0,len(url_list)):
            okay=False
            for j in range(0,global_try_parameter):
                link = self.baseUrl+url_list[i];
                print(link,j)
                headline,summary,text = self.CrawlEachPage(link)
                if(headline != False and summary != False and text != False):
                    okay=True
                    break
                else:
                    print("headline = ",headline)
                    print("summary = ",summary)
                    print("text = ",text)
            if(okay==True):
                print(summary,headline,len(text))
                self.corona_related_tech.Process(date,headline,summary,text,link)

            #debug: print(type(response),len(response))

    def InitiateCrawling(self):
        starting_date = self.starting_date
        number_of_days = self.number_of_days
        l=starting_date.split('/')
        year = l[2]
        month = l[1]
        day = l[0]
        for i in range(0,number_of_days):
            d=datetime.datetime(int(year),int(month),int(day))-datetime.timedelta(days=i)
            d=str(d).split(" ")[0]
            date=d
            l=d.split("-")
            y=int(l[0])
            m=int(l[1])
            d=int(l[2])
            if(len(l[2])<2):
                l[2]="0"+l[2]
            url = self.baseUrl+'/api/list/'+str(y)+'/'+str(m)+'/'+l[2]
            print(date)
            #print(url)
            self.FetchAllLinks(url,str(date))
