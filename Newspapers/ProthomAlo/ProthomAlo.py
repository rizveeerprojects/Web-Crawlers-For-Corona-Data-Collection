#coding: utf-8

from bs4 import BeautifulSoup
from requests import get
import datetime
import os, sys
import json, sys


global_try_parameter=20

class ProthomAlo:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.prothomalo.com"

    def CrawlEachPage(self,link):
        url = link
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        #headline
        try:
            headline = html_soup.find_all('h1',class_='title mb10')
            headline = headline[0].text.strip()
            print(headline)
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = ''
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = html_soup.find('div', attrs={'itemprop':'articleBody'})
            news = news.find_all('p')
            text = ''
            for i in range(0,len(news)):
                text = text + " "+news[i].text
        except Exception as e:
            return headline,summary,False
        #print(headline)
        #print(summary)
        #print(text)
        return (headline,summary,text)

    def FetchAllLinks(self,link,date):
        i=1
        global global_try_parameter
        while True:
            try:
                url = link+'?page='+str(i)
                print(url)
                self.global_saved_urls.append(url)
                response = get(url)
                #print(response)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                a_tags = html_soup.find_all('a',class_='link_overlay')
                print(len(a_tags))
                if(a_tags == "" or len(a_tags)==0):
                    break
                for j in range(0,len(a_tags)):
                    if(a_tags[j]['href'] not in self.global_saved_urls):
                        #print(a_tags[j]['href'])
                        self.global_saved_urls.append(a_tags[j]['href'])
                        for k in range(0,global_try_parameter):
                            url = self.baseUrl+a_tags[j]['href']
                            #print("url = ",url)
                            headline,summary,news = self.CrawlEachPage(url)
                            if(headline != False and summary != False and news != False):
                                #print("YES ",j)
                                break
                        if(headline != False and summary != False and news != False):
                            print("Extracted properly")

                i=i+1
            except Exception as e:
                print(e)
                pass

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
            url = self.baseUrl+'/'+'archive'+'/'+l[0]+"-"+l[1]+'-'+l[2]
            print(date)
            print(url)
            self.FetchAllLinks(url,str(date))
