from bs4 import BeautifulSoup
from requests import post,get
import datetime
import os, sys
import json, sys


global_try_parameter=20

class HindustanTimes:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="http://newssearch.chinadaily.com.cn/"
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}

    def CrawlEachPage(self, url):
        response = get(url,headers=self.headers)
        html_soup = html_soup = BeautifulSoup(response.text, 'html.parser')
        #headline
        try:
            headline = html_soup.find('h1').text
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = html_soup.find('h2').text
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = html_soup.find_all('p', class_="storyDetail")
            text = ""
            for i in range(0,len(news)):
                text = text + " " + news[i].text
        except Exception as e:
            return headline,summary,False
        print(headline)
        print(summary)
        print(text)
        return (headline,summary,text)

    def DotToSlashConversion(self,d):
        l=d.split('.')
        d=l[2]+'-'+l[1]+'-'+l[0]
        return d

    def ReturnMonthID(self, string):
        list = ['Jan','Feb','Mar','Apr', 'May', "Jun", "Jul","Aug","Sep","Oct","Nov","Dec"]
        for i in range(0,len(list)):
            if(list[i] == string):
                if(len(str(i+1))<2):
                    return "0"+str(i+1)
                return str(i+1)

    def FetchAllLinks(self,valid_dates):
        global global_try_parameter
        count = 0
        while True:
            count = count + 1
            link = 'https://www.hindustantimes.com/search?q=corona+virus&pageno='+str(count)
            found = 0
            for i in range(0,global_try_parameter):
                response = get(link,headers=self.headers)
                print(link)
                print(response)
                if(response.status_code == 200):
                    found = 1
                    break
            if(found == 0):
                break
            html_soup = BeautifulSoup(response.text, 'html.parser')
            divs = html_soup.find_all('div',class_='media-heading headingfour')
            a_tags = []
            found_dates = []
            processed_dates = []
            for div in divs:
                a_tags.append(div.find('a')['href'])
            span_tags = html_soup.find_all('span',class_='time-dt')
            for span in span_tags:
                d = span.text
                d = d.split(" ")
                d = d[0:len(d)-1]
                d[1] = d[1].replace(",","")
                month = self.ReturnMonthID(d[0])
                date_object = datetime.datetime(int(d[2]),int(month),int(d[1]))
                found_dates.append(date_object)
                processed_dates.append(d[1]+'/'+month+'/'+d[2])
            break_status = True
            final_a_tags = []
            final_processed_dates = []
            for i in range(0,len(found_dates)):
                if(found_dates[i] <= valid_dates[0] and found_dates[i] >= valid_dates[len(valid_dates)-1]):
                    print(found_dates[i],valid_dates[0],valid_dates[len(valid_dates)-1])
                    final_a_tags.append(a_tags[i])
                    final_processed_dates.append(processed_dates[i])
                    break_status = False
                elif(found_dates[i]<valid_dates[len(valid_dates)-1]):
                    continue

            for i in range(0,len(final_a_tags)):
                headline, summary, news = "", "",""
                for j in range(0,global_try_parameter):
                    print(final_a_tags[i])
                    headline, summary, news = self.CrawlEachPage(final_a_tags[i])
                    if(headline != False and summary != False and news != False):
                        break
                if(headline != False and summary != False and news != False):
                    self.corona_related_tech.Process(final_processed_dates[i], headline, summary, news, final_a_tags[i])
            if(break_status == True):
                break


    def InitiateCrawling(self):
        starting_date = self.starting_date
        number_of_days = self.number_of_days
        l=starting_date.split('/')
        year = l[2]
        month = l[1]
        day = l[0]
        valid_dates=[]
        for i in range(0,number_of_days):
            d=datetime.datetime(int(year),int(month),int(day))-datetime.timedelta(days=i)
            valid_dates.append(d)
        self.FetchAllLinks(valid_dates)
