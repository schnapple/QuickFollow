from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import random
import sys
from os import path
from UserAccount import UserAccount
from MixcloudProcess import MixcloudProcess
from InstagramProcess import InstagramProcess



# Login Process
def login(account):
    process.runLogin(webdriver, account)

def followByUser(person, account, stopFlag):
    return process.runFollowersFollow(webdriver, person, account, stopFlag)

def followByHashtag(hashtag, account, stopFlag):
    return process.runHashtagFollow(webdriver, hashtag, account, stopFlag)


def parseUserDoc(commandPath):
    accounts = []
    accountDoc = open(commandPath+"/Admin/account-info/accountInfo.txt","r")
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
        accounts = parseUserDoc(commandPath)
    sleep(3)
    curAccount = getTargetAccount(accounts, accountID)
    
    chromedriver_path = commandPath+'Bot/chromedriver.exe'
    print('Quick Follow is Running %s Version' %(curAccount.accountType))
    accountInfo(curAccount)
    webdriver = webdriver.Chrome(executable_path=chromedriver_path)
    stopFlag = True
    if curAccount.accountType == 'Mixcloud':
        process = MixcloudProcess()
        login(curAccount)
        for person in curAccount.users:
            if random.randint(0,10) > 4:
                stopFlag = followByUser(person, curAccount, stopFlag)
    else:
        process = InstagramProcess()
        login(curAccount)
        for hashtag in curAccount.hashtags:
            if random.randint(0,10) > 0:
                stopFlag = followByHashtag(hashtag, curAccount, stopFlag)
    
    exit()