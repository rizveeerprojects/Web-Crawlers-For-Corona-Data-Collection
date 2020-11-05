from bs4 import BeautifulSoup
from requests import post,get
import datetime
import os, sys
import json, sys


global_try_parameter=5

class Hindu:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.thehindu.com/"

    def CrawlEachPage(self, url):
        response = get(url)
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
            news_div = html_soup.find_all('div', class_="paywall")
            news = news_div[0].find_all('p')
            text = ""
            for i in range(0,len(news)):
                text = text + " " + news[i].text
        except Exception as e:
            #print(e)
            return headline,summary,False
        print(headline)
        #print(summary)
        #print(text)
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
            link = 'https://www.thehindu.com/topic/coronavirus/?page='+str(count)
            found = 0
            for i in range(0,global_try_parameter):
                response = get(link)
                print(link)
                print(response)
                if(response.status_code == 200):
                    found = 1
                    break
            if(found == 0):
                break
            html_soup = BeautifulSoup(response.text, 'html.parser')
            list = html_soup.find_all('a',class_='Other-StoryCard-heading')
            a_tags = []
            found_dates = []
            processed_dates = []
            for l in list:
                a_tags.append(l['href'])
            print(len(a_tags))
            span_div = html_soup.find_all('div',class_='orgdatecard')
            for div in span_div:
                d = div.find('span').text
                d = d.split(" ")
                month = self.ReturnMonthID(d[1])
                date_object = datetime.datetime(int(d[2]),int(month),int(d[0])) # year, month, day
                found_dates.append(date_object)
                processed_dates.append(d[0]+'/'+month+'/'+d[2])
            break_status = False
            final_a_tags = []
            final_processed_dates = []
            print(len(found_dates))
            for i in range(0,len(found_dates)):
                if(found_dates[i] <= valid_dates[0] and found_dates[i] >= valid_dates[len(valid_dates)-1]):
                    final_a_tags.append(a_tags[i])
                    final_processed_dates.append(processed_dates[i])
                elif(found_dates[i]<valid_dates[len(valid_dates)-1]):
                    print(found_dates[i],valid_dates[len(valid_dates)-1])
                    print("break status true") 
                    break_status = True
                    break
            for i in range(0,len(final_a_tags)):
                headline, summary, news = "", "",""
                for j in range(0,global_try_parameter):
                    print(final_a_tags[i])
                    headline, summary, news = self.CrawlEachPage(final_a_tags[i])
                    if(headline != False and summary != False and news != False):
                        break
                if(headline != False and summary != False and news != False):
                    print(len(news))
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

#hindu = Hindu("","29/10/2020",10)
#hindu.InitiateCrawling()
