from bs4 import BeautifulSoup
from requests import post,get
import datetime
import os, sys
import json, sys


global_try_parameter=20

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
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = json_content['summary']
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = json_content['plainText']
            text = news
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
        count = -1
        while True:
            count = count + 1
            link = 'http://newssearch.chinadaily.com.cn/rest/en/search?keywords=corona%20virus&sort=dp&page='+str(count)+'&curType=story&type=&channel=&source='
            found = 0
            for i in range(0,global_try_parameter):
                response = post(link)
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
                list = json_response['content'][i]['url'].split('/')
                day = list[len(list)-2]
                month = list[len(list)-3][4]+list[len(list)-3][5]
                year = list[len(list)-3][0]+list[len(list)-3][1]+list[len(list)-3][2]+list[len(list)-3][3]
                date_object = datetime.datetime(int(year),int(month),int(day))
                if(date_object<=valid_dates[0] and date_object>=valid_dates[len(valid_dates)-1]): # reverse it is
                    valid_json_content.append(json_response['content'][i])
                    corresponding_dates.append(day+'/'+month+'/'+year)
                elif(date_object<valid_dates[len(valid_dates)-1]):
                    break_status = True
            for i in range(0,len(valid_json_content)):
                print(valid_json_content[i]['url'])
                headline, summary, news = self.CrawlEachPage(valid_json_content[i])
                self.corona_related_tech.Process(corresponding_dates[i],headline,summary,news,valid_json_content[i]['url'])
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
