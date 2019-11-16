from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import random
import sys
from os import path
from UserAccount import UserAccount

# Login Process
def login(account):
    webdriver.get('https://www.mixcloud.com')
    sleep(2)
    login_button_1 = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[3]/div/div/header/div/div[3]/div/span[1]')
    login_button_1.click()
    username = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[1]/div/input')
    username.send_keys(account.username)
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

def followersFollow(person, account):
    commonPath = '/html/body/div[1]/div/section/div[4]/div/div/div/div/div[4]/main'
    sleep(2)      
    webdriver.get('https://www.mixcloud.com/' + person + '/followers/')
    follow_list = webdriver.find_elements_by_xpath(commonPath + '/div[1]/div[2]/ul/li')
    index = 1
    like_count = 0
    follow_doc = open("followList.txt","a")
    while(like_count < int(account.numInteractions)):
        for val in range(index,len(follow_list)):
            if random.randint(0,5) > 2:
                try:
                    follow_button = webdriver.find_element_by_xpath(commonPath + '/div[1]/div[2]/ul/li['+str(val)+']/button')
                    webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)
                    webdriver.execute_script("window.scrollBy(0, -" + str(random.randint(150,200)) + ")")
                    sleep(random.uniform(.5,1))
                    follow_button.click()
                    webdriver.execute_script("window.scrollBy(0, -" + str(random.randint(10,50)) + ")")
                    name = webdriver.find_element_by_xpath(commonPath + '/div[1]/div[2]/ul/li['+str(val)+']/span/b/span/a')
                    follow_doc.write(name.get_attribute("href")+ "," + name.text + '\n')
                    like_count = like_count + 1
                except:
                    print("no follow button: "+str(val))
                webdriver.execute_script("window.scrollBy(0, 200)")
                if(like_count >= int(account.numInteractions)):
                    break
        index = len(follow_list)
        follow_list = webdriver.find_elements_by_xpath(commonPath+'/div[1]/div[2]/ul/li')
    follow_doc.close()

def scroll():
    webdriver.get('https://www.mixcloud.com/DjHIDEKI/followers/')
    follow_button = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li[15]/button')
    sleep(1)
    webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)

def parseUserDoc(commandPath):
    accounts = []
    accountDoc = open(commandPath+"/mix_cloud/bot_docs/accountInfo.txt","r")
    for line in accountDoc.readlines():
        split = line.rstrip().split(',')
        hashtags = []
        for val in split[5].split('||'):
            hashtags.append(val)
        account = UserAccount(split[0],split[1],split[2],split[3],split[4], hashtags[1:], split[6])
        accounts.append(account)
    accountDoc.close()
    return accounts

def accountInfo(account):
    print("\nAccount " + account.username)
    print("Like Percentage: " + account.likePercentage)
    print("Comment Percentage: " + account.commentPercentage)
    print("Num Accounts to Interact: " + account.numInteractions)
    print("Hashtags Searches: " + str(account.hashtags))
    
def getDefault(accounts):
    for account in accounts:
        if int(account.default) == 1:
            return account
    print('NO DEFAULT ACCOUNT RUN ADMIN SCRIPT. Admin.py')
    exit


if __name__ == "__main__":
    print('Mixcloud Quick Follow')
    commandPath = "C:/Users/plagambino/Documents/Other_Work/QuickFollow/"
    if len(sys.argv) > 1:
        commandPath = sys.argv[1]
    if not path.exists(commandPath+"mix_cloud/bot_docs/accountInfo.txt"):
        print('NO BOTS RUN ADMIN SCRIPT. Admin.py')
        exit()
    else:
        accounts = parseUserDoc(commandPath)
    chromedriver_path = commandPath+'Bot/chromedriver.exe' 
    defaultAccount = getDefault(accounts)
    accountInfo(defaultAccount)
    webdriver = webdriver.Chrome(executable_path=chromedriver_path)
    login(defaultAccount)
    for person in defaultAccount.hashtags:
        if random.randint(0,10) > 6:
            followersFollow(person, defaultAccount)
    