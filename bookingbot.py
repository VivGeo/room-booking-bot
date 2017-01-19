#Logs into RULA, shows the available rooms


#Imports
import getpass
from datetime import date
from selenium import webdriver

#Functions

#returns the correct number of days in the month
def getDays ( num ):
    months31 = [1,3,5,7,8,10,12]
    if num in months31:
        print(31)
        return 31
    elif num == 2:
        print(28)
        return 28
    else:
        print(30)
        return 30
    
#Main code

#User credentials
name = input("username: ")
password = getpass.getpass("password: ")
today = date.today()
day = input("Day of the Month: ")


year = today.year
month = today.month

#Opens an instance of chrome
browser = webdriver.Chrome()
#Goes to room booking webpage
browser.get("http://apps.library.ryerson.ca/room_booking/")
#Login Credentials (Change to input style)
userNameElem = browser.find_element_by_id('username')
userNameElem.send_keys(name)
passwordElem = browser.find_element_by_id("password")
passwordElem.send_keys(password)
linkElem = browser.find_element_by_id('submit')
linkElem.click()
#Gets to the desired date (TODO: Change to input)
browser.get('http://apps.library.ryerson.ca/room_booking/booking/booking_main?month=' + str(year) + str(month) + '&date=' + str(year) + str(month) + str(day))
#Selects my study group's room booking criteria (5-8 ppl,LCDs, Whiteboard walls)
seatElem = browser.find_element_by_xpath("//input[@value='5-8']").find_element_by_xpath("./..")
seatElem.click()
LCDElem = browser.find_element_by_xpath("//input[@value='3']").find_element_by_xpath("./..")
LCDElem.click()
whiteboardElem = browser.find_element_by_xpath("//input[@value='6']").find_element_by_xpath("./..")
whiteboardElem.click()
