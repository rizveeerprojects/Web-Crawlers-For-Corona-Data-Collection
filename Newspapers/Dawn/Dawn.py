from bs4 import BeautifulSoup
from requests import post,get
import datetime
import os, sys
import json, sys
import time


global_try_parameter=10

class Dawn:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.dawn.com/"

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
            link = 'https://www.dawn.com/trends/coronavirus/'+str(count)
            found = 0
            for i in range(0,global_try_parameter):
                response = get(link)
                print(link)
                #print(response)
                if(response.status_code == 200):
                    found = 1
                    break
            if(found == 0):
                break
            html_soup = BeautifulSoup(response.text, 'html.parser')
            article_tags = html_soup.find_all('article',class_='box story mb-2 pb-2 latest-stories border-b border-b-solid border-b-grey-default sm:border-b-none')
            #print(article_tags)
            list = []
            summary_info = []
            for i in range(0,len(article_tags)):
                link = article_tags[i].find('a',class_='story__link')
                sum = ""
                sum = article_tags[i].find('div',class_='story__excerpt').text
                if(sum == "" or sum == None or len(sum) <=1):
                    continue
                #print(link,sum)
                list.append(link)
                summary_info.append(sum)

            #list = html_soup.find_all('a',class_='story__link')
            a_tags = []
            for l in list:
                a_tags.append(l['href'])
            print(len(a_tags))
            if(len(a_tags) == 0):
                break
            break_status = ""
            ct = 0
            call = 0
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
                    call = call + 1
                    d = d.split(' ')
                    month = int(self.ReturnMonthID(d[1].strip()))
                    year = int(d[2])
                    day = int(d[0])
                    final_processed_date = d[0].strip()+'/'+str(month)+'/'+d[2].strip()
                    date_object = datetime.datetime(year,month,day)
                    print(date_object,valid_dates[0],valid_dates[len(valid_dates)-1])
                    #print(summary_info[i],len(summary_info))
                    if(date_object<=valid_dates[0] and date_object>=valid_dates[len(valid_dates)-1]):
                        print(len(news))
                        break_status= False
                        summary = summary_info[i]
                        self.corona_related_tech.Process(final_processed_date, headline, summary, news, a_tags[i])
                    elif(date_object<valid_dates[len(valid_dates)-1]):
                        break_status = True
                        ct = ct + 1
                        print("break hocchi")
                        break
            if(break_status == True and ct == call):
                print(valid_dates)
                print(date_object)
                print("break status true")
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
