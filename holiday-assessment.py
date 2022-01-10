#!/usr/bin/env python
# coding: utf-8

# In[200]:


import datetime 
import requests
from dataclasses import dataclass, fields
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time


# In[207]:


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
     
    name: str
    date: datetime.datetime
    
    def __str__ (self):
        return f"{self.name}: {self.date.date()}"
        # String output
        # Holiday output when printed.


# In[208]:


test_examples = Holiday("Festivus", datetime.datetime(2022, 12, 21))
print(test_examples)


# In[113]:


testlist = HolidayList()


# In[114]:


for test in test_examples:
    testlist.addHoliday(test)


# In[194]:


testlist.innerHolidays


# In[195]:


type(testlist.innerHolidays[0].date)


# In[413]:


# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------

class HolidayList:
    def __init__(self):
        self.innerHolidays = []
    def convertMonth(month):
        if month == 'Jan':
            return 1
        elif month == 'Feb':
            return 2
        elif month == 'Mar':
            return 3
        elif month == 'Apr':
            return 4
        elif month == 'May':
            return 5
        elif month == 'Jun':
            return 6
        elif month == 'Jul':
            return 7
        elif month == 'Aug':
            return 8
        elif month == 'Sep':
            return 9
        elif month == 'Oct':
            return 10
        elif month == 'Nov':
            return 11
        elif month == 'Dec':
            return 12
        
    def addHoliday(self, holidayObj):
        if isinstance(holidayObj, Holiday):
            self.innerHolidays.append(holidayObj)
            print(f"The holiday {holidayObj} has been added")
        else:
            print("Invalid object type, please try again")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
    def findHoliday(self, HolidayName, Date):
        for holiday in self.innerHolidays:
            if HolidayName == holiday.name and Date == holiday.date:
                return holiday
            else:
                pass
        # Find Holiday in innerHolidays
        # Return Holiday
    def removeHoliday(self, HolidayName, Date):
        for holiday in self.innerHolidays:
            if HolidayName == holiday.name and Date == datetime.ToShortDateString(holiday.date):
                self.innerHolidays.remove(self.findHoliday(HolidayName, Date))
                print(f"The holiday {HolidayName} was removed")
        
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
    def read_json(self):
        with open('holidays.json', 'r') as file:
            holiday_json = json.load(file)
            for holiday in holiday_json['holidays']:
                holiday_entry = Holiday(holiday['name'], holiday['date'])
                self.addHoliday(holiday_entry)
            file.close()

                
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
    def save_to_json(self):
        data = {}
        data['holidays'] = []
        for holiday in self.innerHolidays:
            data['holidays'].append({'name': holiday.name,                                     'date': holiday.date})

        with open('holidays.json', 'rw') as file:
            file.seek(0)
            file.truncate()
            json.dump(data, file)
        file.close()
        print("Data has been saved")
    def scrapeHolidays(self):
        for year in yearlist:
            time.sleep(.1)
            response = requests.get(f'https://www.timeanddate.com/calendar/custom.html?year={year}&country=1&cols=3&hol=33554809&df=1')
            time.sleep(.1)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', attrs = {'class': 'cht lpad'})
            rows = table.find_all('tr')
            for row in rows:
                data = row.find_all('td')
                date = data[0].text
                month_str = date.split(' ')[0]
                month_int = convertMonth(month_str)
                day_str = date.split(' ')[1]
                day_int = int(day_str)
                hol_name = data[1].text
                new_holiday = Holiday(hol_name, datetime.datetime(int(year), month_int, day_int))
                self.innerHolidays.append(new_holiday)
            
                
    def numHolidays(self):
        return len(self.innerHolidays)
        # Return the total number of holidays in innerHolidays
    def filter_holidays_by_week(self, year, weekNum):
        date_list = []
        start_time = datetime.datetime(year, 1, 1)
        end_time = datetime.datetime(year, 12, 31)
        diff = end_time - start_time
        diff_int = diff.days

        date_adder = []
        for day in range(0, diff.days + 1):
            if day <= 360:       
                new_date = start_time + datetime.timedelta(days=day)
                date_adder.append(new_date)     
                if day % 6 == 0:
                    date_list.append(date_adder)
                    date_adder = []
            else:
                new_date = start_time + datetime.timedelta(days=day)
                date_adder.append(new_date)   
                if day == diff.days - 1:
                    date_list.append(date_adder)
        date_list[1].append(date_list[0])
        holidays = list(filter(lambda x: x.date in date_list[weekNum - 1], self.innerHolidays))
        return holidays
    def display_holidays_by_week(self, year, weekNum):
        hol_list = self.filter_holidays_by_week(year, weekNum)
        for h in hol_list:
            print(h)
    def getWeather():
        
        
    


# In[415]:



print(newlist.getWeather())
print(datetime.datetime(2022, 1, 10))
#rint(newlist.getWeather() == datetime.datetime(2022, 1, 10))


# In[ ]:


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


# In[ ]:


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.

