############## Main function of the library #################

from Newspapers.Guardian.Guardian import Guardian
from Newspapers.Publico.Publico import Publico
from Newspapers.Expresso.Expresso import Expresso
from Newspapers.ProthomAlo.ProthomAlo import ProthomAlo
from Newspapers.ChinaDaily.ChinaDaily import ChinaDaily
from Newspapers.Hindu.Hindu import Hindu
from Newspapers.HindustanTimes.HindustanTimes import HindustanTimes
from Newspapers.Dawn.Dawn import Dawn



from CoronaRelatedTech import CoronaRelatedTech
import datetime

class Main():
    def __init__(self):
        pass

    def StartingDayInput(self):
        starting_date=""
        while True:
            starting_date = input('Please Give Starting Date(dd/mm/yy): ')
            l=starting_date.split('/')
            year = l[2]
            month = l[1]
            day = l[0]
            if(len(l[2])!=4):
                print("year need to be of 4 length(ex - 2020)")
                continue
            if(len(l[0])!=2 or int(l[0])<1 or int(l[0])>31):
                print("day need to be of 2 length(append 0 if necessary) and between 1 and 31")
                continue
            if(int(l[1])<0 or int(l[1])>12 or len(l[1]) != 2):
                print("month need to between 1 and 12 and of 2 length(ex - 01/01/2020)")
                continue
            try:
                 datetime.datetime(int(year),int(month),int(day))
                 valid=True
                 break
            except Exception as e:
                valid=False
                print("Error in date input, please follow correctly(ex-01/01/2020)")
                continue
        return starting_date


    def NumberOfDaysInput(self):
        number_of_days=1
        while True:
            number_of_days = input("Number of days to crawl(ex-10): ")
            try:
                number_of_days = int(number_of_days)
                break
            except Exception as e:
                print("Number of days need to be an integer number: ")
        return number_of_days

    def Start(self,newspaper_key):
        self.starting_date = self.StartingDayInput()
        self.number_of_days = self.NumberOfDaysInput()
        if(newspaper_key == 'guardian'):
            self.corona_related_tech=CoronaRelatedTech('Guardian','United Kingdom','Keywords-zaber-sir.csv','english')
            guardian = Guardian(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            guardian.InitiateCrawling()
        elif(newspaper_key == 'publico'):
            self.corona_related_tech=CoronaRelatedTech('Publico','Portugal','publico-keywords.csv','portuguese')
            publico = Publico(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            publico.InitiateCrawling()
        elif(newspaper_key == 'expresso'):
            self.corona_related_tech=CoronaRelatedTech('Publico','Portugal','publico-keywords.csv','portuguese')
            expresso = Expresso(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            expresso.InitiateCrawling()
        elif(newspaper_key == 'prothom_alo'):
            self.corona_related_tech=CoronaRelatedTech('Expresso','Portugal','publico-keywords.csv','english') ############
            prothomalo = ProthomAlo(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            prothomalo.InitiateCrawling()
        elif(newspaper_key == 'china_daily'):
            self.corona_related_tech=CoronaRelatedTech('China Daily','China','Keywords-zaber-sir.csv','english') ############
            china_daily = ChinaDaily(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            china_daily.InitiateCrawling()
        elif(newspaper_key == 'hindu'):
            self.corona_related_tech=CoronaRelatedTech('Hindu','India','Keywords-zaber-sir.csv','english') ############
            hindu = Hindu(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            hindu.InitiateCrawling()
        elif(newspaper_key == 'hindustan_times'):
            self.corona_related_tech=CoronaRelatedTech('Hindustan Times','India','Keywords-zaber-sir.csv','english') ############
            hindustan_times = HindustanTimes(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            hindustan_times.InitiateCrawling()
        elif(newspaper_key == 'dawn'):
            self.corona_related_tech=CoronaRelatedTech('Dawn','Pakistan','Keywords-zaber-sir.csv','english') ############
            hindustan_times = Dawn(self.corona_related_tech,self.starting_date,self.number_of_days)
            print("Our crawler will start crawling from date ",self.starting_date, " and will take previous ",str(self.number_of_days)," days news articles data.")
            hindustan_times.InitiateCrawling()



main_function = Main()
#main_function.Start('guardian')
#main_function.Start('publico')
#main_function.Start('hindu')
#main_function.Start('hindustan_times')
#main_function.Start('expresso')
#main_function.Start('prothom_alo')
#main_function.Start('dawn')
main_function.Start('china_daily')
