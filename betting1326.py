import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import xlwings as xw
import pytz
from selenium_stealth import stealth
import xlwings as xw
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import math


options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins-discovery")
# options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--headless")

executable_path=r"chromedriver.exe"

driver = webdriver.Chrome(options=options, service=Service(executable_path))

driver.delete_all_cookies()
driver.implicitly_wait(2)

stealth(driver,
    languages=["en-EN", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)


driver.get('https://www.ethercrash.io/play')

# delay 5 sec
time.sleep(5)

# click "History" button
button = driver.find_element(By.XPATH, "//*[@class='tab col-2 noselect']")
button.click()

time.sleep(10)

maxId = 0

mybalance = 27000
#set start value
start_value = 2
#cashout
cashout = 3
autocash = 1.8
red_counter = 0
bet_counter = 0
betted = False
current_bet = start_value

cashedout = 1

count_three = 0
sheetIndex = 1
# red_counter_limit = 3

# create new excel file
wb = xw.Book()
wb.save(str(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).hour) + "-" + str(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).minute) + "-" + str(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).second) + ".xlsx")

# scrap the bust value
def scrap_bustvalue():
    global maxId
    # global wb
    global button
    gameId_arr = []
    global mybalance
    global start_value
    global cashout
    global red_counter
    global bet_counter
    global betted
    global current_bet
    global cashedout
    global count_three
    global sheetIndex
    # global red_counter_limit


    # get the max value from href
    lnks = driver.find_elements(By.XPATH, "//a[starts-with(@class, 'games-log-')]")
    connectionState = driver.find_element(By.CLASS_NAME, "connection-state").text
    if connectionState != "Connection Lost ...": 
        # get the all busted value of the table
        for lnk in lnks:
            url = lnk.get_attribute('href')
            gameId = re.split(r"([0-9]+)",url)[1]
            gameId_arr.append(int(gameId))

        # sort the array
        gameId_arr.sort()

        # get the new busted value and write the data to excel file
        for gameId in gameId_arr:
            #get the bust value by gameId 
            if gameId > int(maxId):                
                bustValue = driver.find_element(By.XPATH, '//a[@href="/game/'+str(gameId)+'"]').text
                # write the data to excel file

                sht1 = wb.sheets['Sheet1']
                colA = 'A' + str(sheetIndex)
                colB = 'B' + str(sheetIndex)

                sht1.range(colA).value = bustValue

                float_chash = re.sub("[^\d\.]", "", re.split(r"(x)",bustValue)[0])

                if len(float_chash) == 0:
                    float_chash =2
                cashedout = float(float_chash)
            
                print("-------------------------------")               

                if cashedout >= cashout:                

                    count_three += 1              
                    sht1.range(colA).color = (0, 170, 100)
                    sht1.range(colB).color = (0, 170, 100)
                    
                    sht1.range(colB).value = count_three

                else:          
                    sht1.range(colA).color = (170, 90, 50)
                    sht1.range(colB).color = (170, 90, 50)
                    red_counter += 1      




                sheetIndex += 1
                    
                print("count three: ", count_three)
                print("red_counter: ", red_counter)

                maxId = gameId
                # wb.save()
            else:
                continue
    else:
        button.click()
        button.click()
        button.click()

# infinite loop            
while True:
    scrap_bustvalue()
    time.sleep(1)
