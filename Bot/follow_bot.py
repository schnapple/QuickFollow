from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import random
import sys
from os import path
from UserAccount import UserAccount
from MixcloudXcode import MixcloudXcode

xcode = MixcloudXcode()

# Login Process
def login(account):
    webdriver.get('https://www.mixcloud.com')
    sleep(2)
    login_button = webdriver.find_element_by_xpath(xcode.login_button)
    login_button.click()
    email = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[1]/div/input')
    email.send_keys(account.email)
    password = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[2]/div/input')
    password.send_keys(account.password)
    sleep(2)
    password.send_keys(Keys.RETURN)

# User Search
def genreFollow(genre):
    sleep(4)
    search_bar = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/header/div/div[2]/input')
    search_bar.click()
    search_bar.send_keys(genre)
    sleep(2)
    filter_time = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/h1/span/span')
    filter_time.click()
    filter_month = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/h1/span/span[2]/span[1]/span[2]')
    filter_month.click()
    filter_time.click()
    sleep(2)
    follow_list = webdriver.find_elements_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li')
    max_val = len(follow_list)
    for val in range(3,max_val):
        try:
            follow_button = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
            follow_button.click()
            print("Clicked: " + '//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
        except:
            print("no follow button: " + '//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
        sleep(1)

def followersFollow(person, account, stopFlag):
    commonPath = '/html/body/div[1]/div/section/div[4]/div/div/div/div/div[4]/main'
    sleep(2)      
    webdriver.get('https://www.mixcloud.com/' + person + '/followers/')
    follow_list = webdriver.find_elements_by_xpath(commonPath + '/div[1]/div[2]/ul/li')
    index = 1
    like_count = 0
    # follow_doc = open("followList.txt","a")
    while(like_count < int(account.numInteractions)):
        for val in range(index,len(follow_list)):
            if random.randint(0,5) > 2 and stopFlag:
                try:
                    follow_button = webdriver.find_element_by_xpath(commonPath + '/div[1]/div[2]/ul/li['+str(val)+']/button')
                    webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)
                    webdriver.execute_script("window.scrollBy(0, -" + str(random.randint(150,200)) + ")")
                    sleep(random.uniform(.5,6))
                    follow_button.click()
                    sleep(random.uniform(.5,2))
                    follow_text = webdriver.find_element_by_xpath(commonPath + '/div[1]/div[2]/ul/li['+str(val)+']/button/span')
                    print(follow_text.text)
                    if follow_text.text == 'Follow':
                        print('Hit Max follows stopping')
                        stopFlag = False
                        
                    webdriver.execute_script("window.scrollBy(0, -" + str(random.randint(10,50)) + ")")
                    name = webdriver.find_element_by_xpath(commonPath + '/div[1]/div[2]/ul/li['+str(val)+']/span/b/span/a')
                    # follow_doc.write(name.get_attribute("href")+ "," + name.text + '\n')
                    like_count = like_count + 1
                except:
                    print("no follow button: "+str(val))
                webdriver.execute_script("window.scrollBy(0, 200)")
                if(like_count >= int(account.numInteractions)):
                    break
        index = len(follow_list)
        follow_list = webdriver.find_elements_by_xpath(commonPath+'/div[1]/div[2]/ul/li')
    # follow_doc.close()
    return stopFlag

def scroll():
    webdriver.get('https://www.mixcloud.com/DjHIDEKI/followers/')
    follow_button = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li[15]/button')
    sleep(1)
    webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)

def parseUserDoc():
    accounts = []
    accountDoc = open("../Admin/account-info/accountInfo.txt","r")
    for line in accountDoc.readlines():
        split = line.rstrip().split(',')
        hashtags = []
        for val in split[4].split('||'):
            hashtags.append(val)
        users = []
        for val in split[5].split('||'):
            users.append(val)
        account = UserAccount(split[0],split[1],split[2],split[3],hashtags[1:], users[1:], split[6])
        accounts.append(account)
    accountDoc.close()
    return accounts

def accountInfo(account):
    print("\nAccount " + account.email)
    print("AccountType: " + account.accountType)
    print("Num Interactions: " + account.numInteractions)
    print("Hashtags Searches: " + str(account.hashtags))
    print('Follow Account: ' + str(account.users))
    print("ID Value: " + str(account.id))
    
def getTargetAccount(accounts, accountID):
    for account in accounts:
        if account.id == accountID:
            return account
    print('NO DEFAULT ACCOUNT RUN ADMIN SCRIPT. Admin.py')
    exit()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        commandPath = sys.argv[1]
        accountID = sys.argv[2]
    else:
        print('NOT ENOUGH ARGS. Need path working directory and User ID. Admin.py')
        exit()
    if  not path.exists(commandPath+"Admin/account-info/accountInfo.txt"):
        print('Incorrect Account Info Path! Run Admin.py')
        exit()
    else:
        accounts = parseUserDoc()
    curAccount = getTargetAccount(accounts, accountID)
    chromedriver_path = commandPath+'Bot/chromedriver.exe' 
    print('Quick Follow is Running %s Version' %(curAccount.accountType))
    accountInfo(curAccount)
    webdriver = webdriver.Chrome(executable_path=chromedriver_path)
    login(curAccount)
    stopFlag = True
    for person in curAccount.users:
        if random.randint(0,10) > 4:
            stopFlag = followersFollow(person, curAccount, stopFlag)
    exit()