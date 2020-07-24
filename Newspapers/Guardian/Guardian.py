from bs4 import BeautifulSoup
from requests import get
import datetime
import os, sys

"""
current_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
sys.path.append(os.path.normpath(os.path.join(current_dir, '..', '..')))
from CoronaRelatedTech import CoronaRelatedTech
"""
global_try_parameter=20

class Guardian:
    def __init__(self,corona_related_tech,starting_date,number_of_days):
        self.corona_related_tech = corona_related_tech
        self.starting_date = starting_date
        self.number_of_days = number_of_days
        self.global_saved_urls=[]
        self.baseUrl="https://www.theguardian.com/theguardian/"

    def CrawlEachPage(self,link):
        url = link
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        #headline
        try:
            headline = html_soup.find_all('h1')
            headline = headline[0].text.strip()
        except Exception as e:
            return False,'',''

        #summary
        try:
            summary = html_soup.find('div',class_='content__standfirst', attrs={'data-link-name':'standfirst','data-component':'standfirst'}).text.strip()
            summary.replace('Coronavirus – latest updates'," ")
            summary.replace('See all our coronavirus coverage'," ")
        except Exception as e:
            return headline,False,''

        #news
        try:
            news = html_soup.find('div',class_='content__article-body from-content-api js-article__body',attrs={'itemprop':'articleBody','data-test-id':'article-review-body'})
            news = news.find_all('p')
            text = ''
            for i in range(0,len(news)):
                text = text + " "+news[i].text
        except Exception as e:
            return headline,summary,False
        return (headline,summary,text)

    def FetchAllLinks(self,link,date):
        url = link
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = html_soup.find_all('a', class_ = 'u-faux-block-link__overlay js-headline-text',attrs={'data-link-name':'article'})
        for i in range(0,len(a_tags)):
            print(a_tags[i]['href'])
            if(a_tags[i]['href'] in self.global_saved_urls):
                continue
            self.global_saved_urls.append(a_tags[i]['href'])
            headline,summary,text = self.CrawlEachPage(a_tags[i]['href'])
            okay = True
            if(headline == False or summary == False or text == False):
                okay=False
                for j in range(1,global_try_parameter):
                    headline,summary,text = self.CrawlEachPage(a_tags[i]['href'])
                    if(headline != False and summary != False and text != False):
                        okay=True
                        break
                if(okay==False):
                    pass
                    #print(headline,summary,text)
            if(okay==True):
                #print(headline)
                #print(summary)
                #print(len(text))
                self.corona_related_tech.Process(date,headline,summary,text,str(a_tags[i]['href']))

    def MonthConverter(self,m):
        list=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        return list[m-1]

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
            url = self.baseUrl+str(y)+'/'+self.MonthConverter(m)+'/'+l[2]
            print(date)
            #print(url)
            self.FetchAllLinks(url,str(date))
            #FetchAllLinks("https://www.theguardian.com/theguardian/2020/jun/22");



#guardian = Guardian(corona_related_tech,'01/01/2020',1)
#guardian.InitiateCrawling()

#StartingDayInput()
#NumberOfDaysInput()
#print("Our crawler will start crawling from date ",starting_date, " and will take previous ",str(number_of_days)," days news articles data.")
#InitiateCrawling()
