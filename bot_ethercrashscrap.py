import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import xlwings as xw
import pytz
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service


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

# driver.get("https://www.ethercrash.io/")
# time.sleep(2)
# #click login
# loginbutton = driver.find_element(By.LINK_TEXT, "Log in").click()

# time.sleep(1)

# login_uname = driver.find_element(By.NAME, "username")
# login_uname.send_keys("namanuisege")
# login_pwd = driver.find_element(By.NAME, "password")
# login_pwd.send_keys("kfesCPiztM")


# time.sleep(10)

driver.get('https://www.ethercrash.io/play')

# delay 5 sec
time.sleep(5)

# click "History" button
button = driver.find_element(By.XPATH, "//*[@class='tab col-2 noselect']")
button.click()

maxId = 0
sheetIndex = 1

bet_values = [20, 1, 1, 200, 400, 4000, 8000, 8000, 100, 1]
cashout_values = [1.25,20,20,1.1,1.55,1.16,1.6,2.7,1.25,10]
red_counter = 0
current_bet = 0
current_cashout = 0
check_red_color = True

# create new excel file
wb = xw.Book()
wb.save(str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))+"ether value.xlsx")

# scrap the bust value
def scrap_bustvalue():
    global maxId
    global sheetIndex
    global wb
    global button
    gameId_arr = []
    global bet_values
    global cashout_values
    global red_counter
    global current_bet
    global current_cashout
    global check_red_color

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
                print(bustValue)
                # write the data to excel file
                sht1 = wb.sheets['Sheet1']
                colA = 'A' + str(sheetIndex)
                colB = 'B' + str(sheetIndex)
                colC = 'C' + str(sheetIndex)
                colD = 'D' + str(sheetIndex)
                colE = 'E' + str(sheetIndex)

                sht1.range(colA).value = bustValue
                sht1.range(colB).value = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
                sht1.range(colC).value = current_bet
                sht1.range(colD).value = current_cashout

                # if check_red_color == False:
                #     sht1.range(colE).value = current_bet * (current_cashout -1)
                # else:
                #     sht1.range(colE).value = -current_bet 

                # change the color of text 
                # red color if value is under 2
                # green color if value is over 2
                float_chash = re.sub("[^\d\.]", "", re.split(r"(x)",bustValue)[0])

                if len(float_chash) == 0:
                    float_chash =0
                cashedout = float(float_chash)

                print("----------------------------")

                print("bet: ", current_bet, " , cashout:", current_cashout)

                # bet_size = driver.find_element(By.NAME, "bet-size")
                # cash_out = driver.find_element(By.NAME, "cash-out")
                # button_bet = driver.find_element(By.CLASS_NAME, "bet-button")
                
                if cashedout >= cashout_values[red_counter]:                
                    sht1.range(colA).color = (0, 170, 100)
                    sht1.range(colB).color = (0, 170, 100)
                    sht1.range(colC).color = (0, 170, 100)
                    sht1.range(colD).color = (0, 170, 100)

                    check_red_color = False

                    current_bet = bet_values[0]
                    current_cashout = cashout_values[0]

                    # if cash_out.is_enabled() == True:
                    #     bet_size.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                    #     bet_size.send_keys(current_bet)
                    #     cash_out.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                    #     cash_out.send_keys(current_cashout)

                    #     time.sleep(0.1)   

                        # button_bet.click()

                    red_counter = 0

                else:
                    sht1.range(colA).color = (170, 90, 50)
                    sht1.range(colB).color = (170, 90, 50)
                    sht1.range(colC).color = (170, 90, 50)
                    sht1.range(colD).color = (170, 90, 50)

                    check_red_color = True

                    if len(float_chash) > 0:
                        red_counter += 1    
                    print(red_counter, " red ")

                    # if cash_out.is_enabled() == True:
                    current_bet = bet_values[red_counter]
                    current_cashout = cashout_values[red_counter]

                    #     if cash_out.is_enabled() == True:
                    #         bet_size.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                    #         bet_size.send_keys(current_bet)
                    #         cash_out.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                    #         cash_out.send_keys(current_cashout)

                    #         time.sleep(0.1)
                    
                            # button_bet.click()


                sheetIndex += 1
                maxId = gameId
                wb.save()
            else:
                continue
    else:
        button.click()
        button.click()
        button.click()

# infinite loop            
while True:
    scrap_bustvalue()
    time.sleep(5)
