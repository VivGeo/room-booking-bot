# Logs into RULA, shows the available rooms


# Imports
import getpass
from datetime import date

from bs4 import NavigableString
from selenium import webdriver
from bs4 import BeautifulSoup


# Functions

# returns the correct number of days in the month
def getDays(num):
    months31 = [1, 3, 5, 7, 8, 10, 12]
    if num in months31:
        print(31)
        return 31
    elif num == 2:
        print(28)
        return 28
    else:
        print(30)
        return 30


# used to check descendants
def getRoomNames(tag):
    if tag.has_attr('class') and tag['class'] == 'table_cell_height':
        return True
    else:
        return False


# Main code

# User credentials
name = input("username: ")
password = getpass.getpass("password: ")
today = date.today()
day = input("Day of the Month: ")
time = input("Time: ")
year = today.year
month = today.month
if int(day) < today.day:
    if month == 12:
        month = 1
    else:
        month = today.month + 1
else:
    month = today.month
num_seats = input("number of seats (5/8):")  # the whiteboard & LCD Panel rooms only come in these sizes
if num_seats != "5" and num_seats != "8":
    num_seats = "5"
# if month is single, pad with left zero
if month < 10:
    month = "0" + str(month)

# Opens an instance of chrome
browser = webdriver.Chrome()
# Goes to room booking webpage
browser.get("http://apps.library.ryerson.ca/room_booking/")
# Login Credentials (Change to input style)
user_name_elem = browser.find_element_by_id('username')
user_name_elem.send_keys(name)
password_elem = browser.find_element_by_id("password")
password_elem.send_keys(password)
link_elem = browser.find_element_by_name('submit')
link_elem.click()
browser.get(
    'http://apps.library.ryerson.ca/room_booking/booking/booking_main?month=' + str(year) + str(month) + '&date=' +
    str(year) + str(month) + str(day))
# Selects my study group's room booking criteria (5-8 ppl,LCDs, Whiteboard walls)
seat_elem = browser.find_element_by_xpath("//input[@value='5-8']").find_element_by_xpath("./..")
seat_elem.click()
seat_elem = browser.find_element_by_xpath("//input[@value='3']").find_element_by_xpath("./..")
seat_elem.click()
white_board_elem = browser.find_element_by_xpath("//input[@value='6']").find_element_by_xpath("./..")
white_board_elem.click()

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

room_found = False
# todo: by selecting for data-seats, the other room picking criteria is neglected, make sure to check for resources
els = soup.find_all(attrs={"data-seats": num_seats})
for el in els:
    available_times = []
    for child in el.children:
        if child.has_attr('class') and 'room_free' in child['class']:
            current_time = str(child.contents[0].contents[0].string.encode('utf-8'))
            if time in current_time:
                print(str(el.contents[0].contents[0].string.encode('utf-8')) + " is available at this time")
                room_found = True;

if room_found is False:
    print("No rooms found")
