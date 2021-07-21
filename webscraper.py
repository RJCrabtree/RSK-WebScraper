from selenium import webdriver # will need to pip install and also download chrome driver
import csv
from datetime import datetime
import pandas as pd # will need to pip install.
from selenium.common.exceptions import NoSuchElementException
import xlwt

driver = webdriver.Chrome('/Users/dianacrabtree/Downloads/chromedriver') # MacOS Path was bugging, so had to specify location of chrome driver

driver.get("https://www.identityserver.com/articles") # base website that program is scraping

check = True

with open('information.csv', 'w') as out: # creating the csv file, allowing file to be written into
    csv_out=csv.writer(out)
    csv_out.writerow(['Author Name', 'Article Name', 'Article Link', 'Published Date']) # specifying the header rows.
    
    while check == True: # checks that the there is a next page, working from code below
        firstname = driver.find_elements_by_css_selector("meta[itemprop='givenName']") # seraches website for the css meta, where itemprop = 'givenName'
        surname = driver.find_elements_by_css_selector("meta[itemprop='familyName']")
        published = driver.find_elements_by_css_selector("meta[itemprop='datePublished']")
        titles = driver.find_elements_by_css_selector("h3[itemprop='name headline']")
        elems =  driver.find_elements_by_tag_name("Ul>li>article>a") # tagline path, instead of returning all the elements with a, by specifying we only get the specific ones we want.

        for f,s,dp,t,l in zip(firstname, surname, published, titles, elems): # iterate through one of each
            firstnameTemp = f.get_attribute("content") # temporarly saves the first attribute element for the first name found in driver.find
            surnameTemp = s.get_attribute("content")
            datePublishedTemp = dp.get_attribute("content")
            articleTitleTemp = t.get_attribute("innerHTML")
            articleLinkTemp = l.get_attribute("href")
            AuthorNameConcatonated = firstnameTemp + ' ' + surnameTemp # concatonates the first and last name

            date_time = datePublishedTemp

            date_object = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S") 

            timestamp = datetime.timestamp(date_object) # convert to timestamp

            date_time = datetime.fromtimestamp(timestamp) # convert back to date time

            date = date_time.strftime("%d/%m/%Y") # specifiying formate of day, month, year

            outputTuple = (AuthorNameConcatonated,articleTitleTemp,articleLinkTemp,date) # creates tuple of the information

            csv_out.writerow(outputTuple) # writes the tuple to the csv file

        try:
            driver.find_element_by_xpath("/html/body/main/div[2]/div/div/aside[2]/p[3]/a").click() # checks to see if there is a next page by searching for X path of button
        except NoSuchElementException: # if no X path, error is thrown. This stop the code from breaking and contines
            check = False
            break

dataframe = pd.read_csv("information.csv") # turns the csv file into dataframe format

sorted_dataframe = dataframe.sort_values(by=['Author Name', 'Published Date'] , ascending = True)
   
sorted_dataframe.to_csv('information.csv', index=False) # rewrites the csv in orderd file, in dataframe format ready to be put exported to excel. (Index is off since this would index every input).

wb = xlwt.Workbook()
sh = wb.add_sheet('information')

with open('information.csv', 'r') as f: # opens csv in read only as f
    reader = csv.reader(f) # returns reader object
    for r,row in enumerate(reader): # gives reader a counter to iterable, itereates through the rows in the csv
        for c,val in enumerate(row):
            sh.write(r,c,val) # writes to sh, which then saves to the wb since sh calls wb.

wb.save('information.xls') # saves the wb

driver.close() # closes driver (web page) once all is complete
