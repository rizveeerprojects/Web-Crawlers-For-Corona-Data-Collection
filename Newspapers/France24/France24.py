from bs4 import BeautifulSoup
from requests import post,get
import datetime
import os, sys
import json, sys
import time


global_try_parameter=10

class France24:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.france24.com/"

    def CrawlEachPage(self, url):
        response = get(url)
        html_soup = html_soup = BeautifulSoup(response.text, 'html.parser')

        # date
        try:
            span_tag = html_soup.find_all('span',class_='story__time')[0]
            d = span_tag.text.strip()
            d = d.replace(','," ")
            d = d.replace('\n'," ")
            d = d.split(' ')
            month = ""
            #print(d)
            for i in range(0,len(d)):
                try:
                    value = int(d[i])
                    if(value>=1 and value<=31):
                        day = d[i]
                    elif(value>=2000):
                        year = d[i]
                except Exception as e:
                    try:
                        result = self.ReturnMonthID(d[i])
                        if(result != None):
                            month = d[i]
                    except Exception as e:
                        continue
            #print(day,month,year)
            d = day+" "+month+" "+year
            print(d)
        except Exception as e:
            print("date e error")
            print(e)
            return False,'','',False

        #headline
        try:
            headline = html_soup.find('h2',class_='story__title')
            headline = headline.find('a',class_='story__link').text
            print(headline)
        except Exception as e:
            print("headline e bug")
            print(e)
            return False,'','',d

        #summary
        try:
            summary = ""  #html_soup.find('h2').text
        except Exception as e:
            return headline,False,'',d

        #news
        try:
            news_div = html_soup.find_all('div', class_="story__content")
            news = news_div[0].find_all('p')
            text = ""
            for i in range(0,len(news)):
                text = text + " " + news[i].text
        except Exception as e:
            print("news e bug")
            print(e)
            return headline,summary,False,d

        #print(headline)
        #print(summary)
        #print(text)
        return (headline,summary,text,d)

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
        return None

    def FetchAllLinks(self,valid_dates):
        global global_try_parameter
        count = 0
        while True:
            count = count + 1
            if(count==1):
                link = 'https://www.france24.com/en/tag/coronavirus/#pager'
            else:
                link =  'https://www.france24.com/en/tag/coronavirus/'+str(count)+'/#pager'
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
            divs = html_soup.find_all('div',class_='m-item-list-article')

            a_tags = []
            dates = []
            for i in range(0,len(divs)):
                a_tags.append(divs[i].find('a').href)
                dates.append(divs[i].find('time').text)

            """
            a_tags = []
            for l in list:
                a_tags.append(l['href'])
            """
            print(len(a_tags))

            break_status = True
            for i in range(0,len(a_tags)):
                print(a_tags[i])
                headline, summary, news, d = "", "","",""
                for j in range(0,global_try_parameter):
                    headline, summary, news, d = self.CrawlEachPage(a_tags[i])
                    if(d == False):
                        time.sleep(.500)
                        continue
                    if(headline != False and summary != False and news != False):
                        break
                if(headline != False and summary != False and news != False and d != False):
                    d = d.split(' ')
                    month = int(self.ReturnMonthID(d[1].strip()))
                    year = int(d[2])
                    day = int(d[0])
                    final_processed_date = d[0].strip()+'/'+str(month)+'/'+d[2].strip()
                    date_object = datetime.datetime(year,month,day)
                    print(summary_info[i],len(summary_info))
                    if(date_object<=valid_dates[0] and date_object>=valid_dates[len(valid_dates)-1]):
                        print(len(news))
                        break_status= False
                        summary = summary_info[i]
                        self.corona_related_tech.Process(final_processed_date, headline, summary, news, a_tags[i])
                    elif(date_object<valid_dates[len(valid_dates)-1]):
                        break_status = True
                        break
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

france24 = France24("","29/10/2020",10)
france24.InitiateCrawling()
