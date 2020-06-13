# Web-Crawlers-For-Corona-Data-Collection
This repository is developed for the collection of corona related data from newspaper, web pages, important articles through diffrent types of crawlers. Main goal is to collect and visualize COVID-19 related information appeared in different sources. Currently we include the crawleres for the following papers. 

* The Guardian 
* The New York Times 
* The Prothom Alo (currently under development)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.


### Prerequisites
The requirements to run this project are given following - 
```
Windows 7,8,10 / Linux
```
```
Java Version 14
```
```
Python Version 3.x; x>=6
```

### Installation
Create a directory and go there. Open your terminal and type the following command. If you are not comfortable with using terminal, please download this repository as zip from the above option and unzip it within the created directory.

```
git clone https://github.com/rizveeerprojects/Web-Crawlers-For-Corona-Data-Collection.git
```

## Running the Crawlers 

* Go to your desired newspaper folder(Guardian, New-York-Times etc.) 
* Within your folder, you will get a script(.sh) file. Run it. Newspaper crawling will start. All sorts of news of the respective newspaper will be saved into the respective csv file in your current folder. 
* In the file "processed_dates.txt", we keep the dates of which the crawler collected all the newses. So, for each run of the script our crawler first collects all the news from current day up to the last day stored into the file.
* In the '.java' file, there is a variable named 'number_of_backward_days'. The value of this variable is currently set to 10. It means that from the oldest day saved into the "processed_dates.txt" file, our crawler runs and collects more 10 days newses previous to this date. You can increase the variable to collect more old newses. 
```
number_of_backward_days=10; //change this if you want to collect more old days newses
```
* After extracting the newses and saving them into respective csv file, return to the home directory of the project. 
* In 'InformationExtraction.py' file, in line 31, you will provide the respective csv file's path link. 
```
file_urls =['E:/Research/Web-Crawlers-For-Corona-Data-Collection/Newspapers/Guardian/guardian_data_news_data.csv']
paper_country_list = ['UK']
paper_name_list = ['Guardian']
```
* Now run the script 'informationExtraction.sh'. From provided csv file's link, it will extract the corona related newses based on the keywords provided in 'Keywords.csv' file. Update it, if you want to change the keywords. 
* If all the corona related news extracted from the csv file's link (which you set), you can clear the csv file before next use so that repeated information are not extracted again. The complete extracted information will be saved into project's home directory's 'Extracted Information.csv' file. Feel free to use this file. 

## Authors 
* **[Redwan Ahmed Rizvee](https://www.facebook.com/profile.php?id=100007730446852)**

## Acknowledgments
This is an ongoing research project to collect data related to the novel coronavirus appearing in the newspapers of different countries. Feel free to provide your suggestions and comments. For any issue please mail [rizveeredwan.csedu@gmail.com](https://www.linkedin.com/in/redwan-ahmed-rizvee-303b68133/). 




