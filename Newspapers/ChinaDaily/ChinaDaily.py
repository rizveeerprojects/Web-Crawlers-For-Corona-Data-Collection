from bs4 import BeautifulSoup
from requests import post,get
import datetime
import os, sys
import json, sys
import time

global_try_parameter=10

class ChinaDaily:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="http://newssearch.chinadaily.com.cn/"

    def CrawlEachPage(self, json_content):
        #headline
        try:
            headline = json_content['title']
            if(headline =="" or headline == None):
                headline = ""
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = json_content['summary']
            if(summary =="" or summary ==None):
                summary = ""
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = json_content['plainText']
            text = news
            if(text=="" or text==None):
                text = ""
        except Exception as e:
            return headline,summary,False
        #print(headline)
        #print(summary)
        #print(text)
        return (headline,summary,text)

    def DotToSlashConversion(self,d):
        l=d.split('.')
        d=l[2]+'-'+l[1]+'-'+l[0]
        return d

    def FetchAllLinks(self,valid_dates):
        global global_try_parameter
        count = 1830
        while True:
            count = count + 1
            link = 'http://newssearch.chinadaily.com.cn/rest/en/search?keywords=coronavirus&sort=dp&page='+str(count)+'&curType=story&type=&channel=&source='
            found = 0
            for i in range(0,global_try_parameter):
                response = post(link)
                print(response.status_code)
                if(response.status_code == 200):
                    found = 1
                    break
            if(found == 0):
                break
            json_response = response.json()
            valid_json_content = []
            corresponding_dates = []
            break_status = False
            for i in range(0,len(json_response['content'])):
                try:
                    list = json_response['content'][i]['url'].split('/')
                except Exception as e:
                    print(e)
                    print(count)
                    print(json_response['content'][i])
                day = list[len(list)-2]
                l=[]
                print(list)
                if(len(list)<3):
                    continue
                for j in range(0,len(list[len(list)-3])):
                    if(list[len(list)-3][j]>='0' and list[len(list)-3][j]<='9'):
                        l.append(list[len(list)-3][j])
                print(l)
                print(json_response['content'][i]['url'])
                try:
                    year = l[0]+l[1]+l[2]+l[3]
                except Exception as e:
                    print(e)
                    continue
                month = ""
                for j in range(4,len(l)):
                    month = month+l[j]
                year = list[len(list)-3][0]+list[len(list)-3][1]+list[len(list)-3][2]+list[len(list)-3][3]
                try:
                    date_object = datetime.datetime(int(year),int(month),int(day))
                except Exception as e:
                    print(list)
                    print(e)
                print(date_object,json_response['content'][i]['url'],valid_dates[0],valid_dates[len(valid_dates)-1])
                if(date_object<=valid_dates[0] and date_object>=valid_dates[len(valid_dates)-1]): # reverse it is
                    valid_json_content.append(json_response['content'][i])
                    corresponding_dates.append(day+'/'+month+'/'+year)
                elif(date_object<valid_dates[len(valid_dates)-1]):
                    break_status = True
            print(len(valid_json_content),len(json_response['content']))
            for i in range(0,len(valid_json_content)):
                print(valid_json_content[i]['url'])
                for j in range(0,global_try_parameter):
                    try:
                        headline, summary, news = self.CrawlEachPage(valid_json_content[i])
                        if(headline != False and summary != False and news != False):
                            self.corona_related_tech.Process(corresponding_dates[i],headline,summary,news,valid_json_content[i]['url'])
                            break
                    except Exception as e:
                        print("ekhane error")
                        print(e)
                        time.sleep(.500)
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
