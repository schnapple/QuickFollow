from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import random
import datetime
from os import path
from UserAccount import UserAccount

chromedriver_path = 'C:/Users/plagambino/Documents/Other_Work/Bot/chromedriver.exe' 
sleep(1)

# Login Process
def login(selectedAccount):
    webdriver.get('https://www.instagram.com/accounts/login')
    sleep(2)
    username = webdriver.find_element_by_name('username')
    username.send_keys(selectedAccount.username)
    password = webdriver.find_element_by_name('password')
    password.send_keys(selectedAccount.password)
    sleep(2)
    password.send_keys(Keys.RETURN)

def personFollow(person_url, clickedList):
    sleep(2)
    webdriver.get(person_url)
    followerButton = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
    followerButton.click()
    sleep(1)
    follow_list = webdriver.find_elements_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li')
    maxVal = len(follow_list)
    followDoc = open("./bot_docs/masterList.txt","a")
    for index in range(1,10):
        try:
            followButton = webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(index)+']/div/div[3]/button')
            accountName = webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(index)+']/div/div[2]/div[1]/div/div/a')
            webdriver.execute_script("return arguments[0].scrollIntoView();", followButton)
            sleep(random.uniform(0,1))
            if(followButton.text=='Follow' and accountName.text not in clickedList.split(',')[0]):
                followButton.click()
                followDoc.write(accountName.text + ', ' + accountName.get_attribute("href") + datetime.today().strftime('%Y-%m-%d') + '\n')
        except:
            print("no follow button: " + '/html/body/div[3]/div/div[2]/ul/div/li['+str(index)+']/div/div[3]/button')
    followDoc.close()

def accountInteractionHashtag(hashtagUrl, clickedList, selectedAccount):
    sleep(2)
    webdriver.get(hashtagUrl)
    firstPicture = webdriver.find_element_by_xpath('/html/body/span/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    firstPicture.click()
    sleep(1)
    val = 1
    followDoc = open("./bot_docs/masterList.txt","a")
    for index in range(1,int(selectedAccount.numInteractions)):
        hashtagFollow(clickedList, followDoc)
        hashtagLike(selectedAccount.likePercentage)
        # hashtagComment(selectedAccount.commentPercentage)
        nextButton = webdriver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a['+str(val)+']')
        nextButton.click()
        val = 2

    followDoc.close()

def hashtagFollow(clickedList, followDoc):
    sleep(random.uniform(.5,1))
    followButton = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
    accountName = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a')
    if(followButton.text=='Follow' and accountName.text not in clickedList):
        followButton.click()
        followDoc.write(accountName.text + ',' + accountName.get_attribute("href") + ','+ datetime.datetime.today().strftime('%Y-%m-%d') + '\n')

def hashtagLike(likePercentage):
    sleep(random.uniform(.5,1))
    likeButton = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button')
    if(random.randint(0,100)<int(likePercentage)):
        likeButton.click()

def hashtagComment(commentPercentage):
    sleep(random.uniform(.5,1))
    commentButton = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button')
    if(random.randint(0,100)<int(commentPercentage)):
        commentInput = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
        commentInput.send_keys('THAT LOOKS AMAZIN!!')
        postButton = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/button')
        postButton.click()

def formFollowingArray(numFollowing, clickedList):
    sleep(1)
    webdriver.get('https://www.instagram.com/totem_tribe/')
    followingButton = webdriver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[3]/a')
    followingButton.click()
    sleep(1)
    followingList = formAccountArray(']/div/div[1]/div[2]/div[1]/a', numFollowing)
    return followingList

def formFollowerArray(numFollowers):
    sleep(1)
    webdriver.get('https://www.instagram.com/totem_tribe/')
    followerButton = webdriver.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a')
    followerButton.click()
    sleep(1)
    followerList = formAccountArray(']/div/div[2]/div[1]/div/div/a', numFollowers)
    return followerList

def formAccountArray(xpath, numPeople):
    accounts = []
    for index in range(1,numPeople):
        try:
            accountName = webdriver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(index)+xpath)
            webdriver.execute_script("return arguments[0].scrollIntoView();", accountName)
            accounts.append(accountName.text + ',' + accountName.get_attribute("href") )
        except:
            val = 0
    return accounts

def unfollowNonbelievers(followingList, followerList):
    for person in followingList:
        sleep(random.uniform(.5,1))
        if person not in followerList:
            href = person.split(',')[1]
            webdriver.get(href)
            sleep(random.uniform(.2,.7))
            followButton = webdriver.find_element_by_xpath('/html/body/span/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
            followButton.click()
            sleep(random.uniform(.2,.7))
            unfollowButton = webdriver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
            unfollowButton.click()
    
def parseFile():
    clickedList = {}
    followDoc = open("./bot_docs/masterList.txt","r")
    for line in followDoc.readlines():
        split = line.rstrip().split(',')
        clickedList[split[0]] = split[1]
    followDoc.close()
    print(clickedList)
    return clickedList    

def parseUserDoc():
    accounts = []
    accountDoc = open("./bot_docs/accountInfo.txt","r")
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
    print("\nAccount " + account.username + "Details.")
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
    print('Instagram Quick Follow')
    if not path.exists("./bot_docs/accountInfo.txt"):
        print('NO BOTS RUN ADMIN SCRIPT. Admin.py')
        accounts = parseUserDoc()
    else:
        accounts = parseUserDoc()
    defaultAccount = getDefault(accounts)
    accountInfo(defaultAccount)
    webdriver = webdriver.Chrome(executable_path=chromedriver_path)
    login(defaultAccount)
    clickedList = parseFile()
    for hashtag in defaultAccount.hashtags:
        url = 'https://www.instagram.com/explore/tags/' + hashtag + '/'
        accountInteractionHashtag(url, clickedList, defaultAccount)