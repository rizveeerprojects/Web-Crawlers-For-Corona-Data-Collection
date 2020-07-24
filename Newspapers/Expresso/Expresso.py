from bs4 import BeautifulSoup
from requests import get
import datetime
import os, sys
import json, sys


global_try_parameter=20

class Expresso:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://expresso.pt"

    def CrawlEachPage(self,link):
        url = link
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        #headline
        try:
            headline = html_soup.find_all('h1',class_='title')
            headline = headline[0].text.strip()
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = html_soup.find('h2',class_='lead').text.strip()
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = html_soup.find('div',class_='articleContent')
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
                lin = self.baseUrl+url_list[i];
                print(lin,j)
                headline,summary,text = self.CrawlEachPage(lin)
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

    def DotToSlashConversion(self,d):
        l=d.split('.')
        d=l[2]+'-'+l[1]+'-'+l[0]
        return d

    def FetchAllLinks(self,url,date):
        global global_try_parameter
        local_urls=[]
        T=23
        while True:
            if(T<0):
                return
            link = url+str(T)
            response = get(link)
            print(link)
            if(link not in local_urls):
                local_urls.append(link)
            else:
                T=T-1
                continue
            if(response.status_code == 503):
                return
            html_soup = BeautifulSoup(response.text, 'html.parser')
            a_tags=html_soup.find_all('a', attrs={'rel':'canonical'})
            date_tags=html_soup.find_all('p',class_='timeStamp js-relative-time publishedDate')
            dates=[]
            for i in range(0,len(date_tags)):
                dates.append(date_tags[i].text.strip())
            for i in range(0,len(a_tags)):
                d=dates[i].split(' ')[0]
                tim=dates[i].split(' ')[2]
                d=self.DotToSlashConversion(d)
                if(d != date):
                    print(d,date)
                    T = -1
                    return
                T=int(tim.split('h')[0])
                if(a_tags[i]['href'] not in self.global_saved_urls):
                    self.global_saved_urls.append(a_tags[i]['href'])
                    print(a_tags[i]['href'])
                    headline=False
                    summary=False
                    news=False
                    for j in range(0,global_try_parameter):
                        link = self.baseUrl+a_tags[i]['href']
                        try:
                            headline,summary,news = self.CrawlEachPage(link)
                            if(headline != False and summary != False and news != False):
                                break
                        except Exception as e:
                            pass
                    if(headline != False and summary != False and news != False):
                        print(headline,summary,len(news))
                        self.corona_related_tech.Process(date,headline,summary,news,link)

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
            url = self.baseUrl+'/api/molecule/category/coronavirus?offset='+l[0]+'-'+l[1]+'-'+l[2]+'T'
            print(date)
            #print(url)
            self.FetchAllLinks(url,str(date))
