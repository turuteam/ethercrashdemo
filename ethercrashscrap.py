import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
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

driver.get("https://www.ethercrash.io/")
time.sleep(2)
#click login
loginbutton = driver.find_element(By.LINK_TEXT, "Log in").click()

time.sleep(1)

login_uname = driver.find_element(By.NAME, "username")
login_uname.send_keys("namanuisege")
login_pwd = driver.find_element(By.NAME, "password")
login_pwd.send_keys("kfesCPiztM")


time.sleep(10)

driver.get('https://www.ethercrash.io/play')

# delay 5 sec
time.sleep(5)

# click "History" button
button = driver.find_element(By.XPATH, "//*[@class='tab col-2 noselect']")
button.click()

time.sleep(10)

maxId = 0

mybalance = 100000
#set start value
start_value = 10
#cashout
cashout = 3
autocash = 1.8
red_counter = 0
bet_counter = 0
betted = False
current_bet = start_value

cashedout = 1
# red_counter_limit = 3

# create new excel file
# wb = xw.Book()
# wb.save(str(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).hour) + "-" + str(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).minute) + "-" + str(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).second) + ".xlsx")

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


                # change the color of text 
                # red color if value is under 2
                # green color if value is over 2
                float_chash = re.sub("[^\d\.]", "", re.split(r"(x)",bustValue)[0])

                if len(float_chash) == 0:
                    float_chash =2
                cashedout = float(float_chash)

                
                print("-------------------------------")
                print("current balance: ", mybalance)
                if mybalance < 0 :
                    print("you don't have enough balance. Purchase please.")
                    break                


                # bet_size = driver.find_element(By.NAME, "bet-size")
                # cash_out = driver.find_element(By.NAME, "cash-out")
                # if cash_out.is_enabled() == True:
                #     cash_out.clear()
                #     cash_out.send_keys(cashout)

                button_bet = driver.find_element(By.CLASS_NAME, "bet-button")

                if cashedout >= cashout:                

                    red_counter = 0
                    bet_counter = 0
                         
                    mybalance += current_bet * (cashout - 1)
                    current_bet = start_value

                    # if bet_size.is_enabled() == True:
                    #     bet_size.clear()
                    #     bet_size.send_keys(math.ceil(current_bet))


                    print("green Bet  started")
                        # button_bet.click()

                else:          
                    red_counter += 1      
                    print(red_counter, " red ")   
                    
                    mybalance = mybalance - current_bet
                    current_bet = current_bet * autocash
                    print("current_bet in red: ", current_bet)

                    print("what is next bet? ", math.ceil(current_bet))

                    if (red_counter == 1 or red_counter == 2):
                        current_bet =1

                    if red_counter % 5 == 0:
                        current_bet = current_bet / 1.2 
                        print("Bomb ", red_counter)            

                    # if bet_size.is_enabled() == True:
                    #     bet_size.clear()
                    #     bet_size.send_keys(math.ceil(current_bet))
                    print("red Bet  started")

                        # button_bet.click()

                    
                print("bustValue: ", bustValue)
                print("new balance: ", mybalance)

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
    time.sleep(3)
