#!/usr/bin/env python
# coding: utf-8

# In[669]:


import datetime 
import requests
from dataclasses import dataclass, fields
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pprint import pprint


# In[670]:


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
        return f"{self.name}: {self.date}"
        # String output
        # Holiday output when printed.


# In[716]:


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
    def strToDate(self, date):
        try:
            split_str = date.split('-')
            cast_date = datetime.datetime(int(split_str[0]), int(split_str[1]), int(split_str[2]))
            return cast_date
        except:
            print('Incorrect formatting, please try again.')
        
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
            if HolidayName == holiday.name and Date == holiday.date.date():
                self.innerHolidays.remove(self.findHoliday(HolidayName, Date))
                print(f"The holiday {HolidayName} was removed")
        
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
    def read_json(self):
        print("reading json file...")
        time.sleep(1)
        with open('holidays.json', 'r') as file:
            holiday_json = json.load(file)
            for holiday in holiday_json['holidays']:
                holiday_entry = Holiday(holiday['name'], self.strToDate(holiday['date'].split(' ')[0]))
                self.addHoliday(holiday_entry)
            file.close()

                
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
    def save_to_json(self):
        print("Overwriting data...")
        time.sleep(1)
        data = {}
        data['holidays'] = []
        for holiday in self.innerHolidays:
            data['holidays'].append({'name': holiday.name,                                     'date': str(holiday.date)})

        with open('holidays.json', 'w') as file:
            file.seek(0)
            file.truncate()
            json.dump(data, file)
        file.close()
        print("Data has been saved")
    def scrapeHolidays(self):
        print('Scraping holidays from web...')
        yearlist = ['2020', '2021', '2022', '2023', '2024']
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
    def getWeather(self):
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

        querystring = {"q":"Minneapolis","days":"5"}

        headers = {
            'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
            'x-rapidapi-key': "d6018c029fmsh69bf22a36ce922bp1891b1jsn6a958d456fac"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        weather = response.json()

        for day in weather['forecast']['forecastday']:
            date_split = day['date'].split('-')
            cast_date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
            condition = day['day']['condition']['text']
            holidays = list(filter(lambda x: x.date == cast_date, self.innerHolidays))
            print(f"{cast_date.date()}: {holidays}: {condition}")
        
    def viewCurrentWeek(self):
        week_list = []
        a_time = datetime.datetime.today()
        start_time = a_time.replace(hour=0, minute=0, second=0, microsecond=0)
        week_list.append(start_time)
        for i in range(1, 7):
            new_time = start_time + datetime.timedelta(days = i)
            week_list.append(new_time)
        for day in week_list:
            holidays = list(filter(lambda x: x.date == day, self.innerHolidays))
            if len(holidays) == 0:
                print(f"{day.date()}: None")
            else:    
                print(f"{day.date()}: {holidays[0].name}")
        print("Would you like to view the weather forecast? (Y/N)")
        weather_choice = input()
        if weather_choice == 'Y':
            self.getWeather()
        
        
    


# In[725]:


def main():
    print('--------------------------------------')
    print('       Welcome to Holiday Creator     ')
    print('--------------------------------------')
    newlist = HolidayList()
    newlist.read_json()
    #newlist.scrapeHolidays()
    menu = True
    while menu == True:
        print(f"There are {newlist.numHolidays()} holidays in the system")
        print('--------------------------------------')
        print('        Holiday Creator Main Menu     ')
        print('--------------------------------------')
        print('Select an option:')
        print('1. Add a Holiday')
        print('2. Remove a Holiday')
        print('3. Save Holiday List')
        print('4. View Holidays')
        print('5. Exit Program')
        choice = input()
        
        if choice =='1':
            print('Enter the name of the holiday')
            name = input()
            print('Enter the date of the holiday in YYYY-mm-dd format')
            date_str = input()
            date = newlist.strToDate(date_str)
            new_holiday = Holiday(name, date)
            newlist.addHoliday(new_holiday)
            
        if choice == '2':
            print('Enter the name of the Holiday')
            name = input()
            print('Enter the date of the holiday in YYYY-mm-dd format')
            date_str = input()
            date = newlist.strToDate(date_str)
            newlist.removeHoliday(name, date)
            
        if choice == '3':
            print('Are you sure you want to save your changes? (Y/N)')
            yn = input()
            if yn == 'Y':
                newlist.save_to_json()
        
        if choice == '4':
            print('Choose the year you want to view')
            year = int(input())
            print('Choose the week number you want to view')
            week = int(input())
            print(newlist.display_holidays_by_week(year, week))
            time.sleep(1)
            print('Would you like to see the forecast? (Y/N)')
            choice2 = input()
            if choice2 == 'Y':
                newlist.getWeather()
                
        if choice == '5':
            print('Are you sure you want to quit? Any unsaved progress will be lost.')
            yn = input()
            if yn == 'Y':
                menu = False
            
            
            
            
        
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


# In[586]:


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


# In[ ]:




