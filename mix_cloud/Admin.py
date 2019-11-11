from time import sleep, strftime
import random
import datetime
from os import path
from UserAccount import UserAccount

chromedriver_path = 'C:/Users/plagambino/Documents/Other_Work/Bot/chromedriver.exe' 
sleep(1)



def createFollowBotAccount():
    userDoc = open("./bot_docs/accountInfo.txt", "a")
    print('Welcome New Quick Follow User Create Account.')
    print('All this information is stored locally in a text file at this realtive file path ./account_lists/accountInfo.txt. \nKeep that file safe.')
    print('What is your email?')
    username = input()
    print('What is your password?')
    password = input()
    print('What Operation do you want to do?\nFollow, Like, and Comment (1)\nFollow and Like (2)\nFollow (3)')
    operationNum = input()
    while operationNum not in ['1','2','3']:
        print("Incorrect input:" + operationNum + "\n")
        print('What Operation do you want to do?\nFollow, Like, and Comment (1)\nFollow and Like (2)\nFollow (3)')
        operationNum = input()
    if operationNum == '1':
        likePercentage = 50
        commentPercentage = 0
    elif operationNum == '2':
        likePercentage = 50
    print("What hashtag do you want to follow with? (type done to stop)")
    hashtags = []
    hashtag = input()
    while not hashtag == 'done':
        hashtags.append(hashtag)
        print("What hashtag do you want to follow with? (type done to stop)")
        print("Current people: " + str(hashtags))
        hashtag = input()
    formattedHashtags = ''
    for hashtag in hashtags:
        formattedHashtags = formattedHashtags + '||' + hashtag
    print('How many people do you want to interact with per hashtag? (It isn\'t good to go above 10 mixcloud can catch on!)')
    numInteractions = input()
    while not numInteractions.isdigit():
        print('Not an integer!')
        print('How many people do you want to interact per hashtag? (It isn\'t good to go above 10 mixcloud can catch on!)')
        numInteractions = input()
    userDoc.write(username + ',' + password + ',' + str(likePercentage) + ',' + str(commentPercentage) + ',' + str(numInteractions) + ',' + formattedHashtags + ',' + str(0)+'\n')
    userDoc.close()

def selectDefaultUser(accounts):
    print()
    for i in range(0,len(accounts)):
        print(str(i) + ": " + accounts[i].username)
    print("Select Account Index")
    accountNum = input()
    while not accountNum.isnumeric() or int(accountNum) not in range(0,len(accounts)):
        print("Invalid Input")
        for i in range(0,len(accounts)):
            print(str(i) + ": " + accounts[i].username)
        accountNum = input()
    for account in accounts:
        account.default = 0
    accounts[int(accountNum)].setDefault()
    return accounts[int(accountNum)]

def writeUserDoc(accounts):
    userDoc = open("./bot_docs/accountInfo.txt", "w")
    for account in accounts:
        formattedHashtags = ''
        for hashtag in account.hashtags:
            formattedHashtags = formattedHashtags + '||' + hashtag
        userDoc.write(str(account.username) + ',' + str(account.password) + ',' + str(account.likePercentage) + ',' + str(account.commentPercentage) + ',' + str(account.numInteractions) + ',' + str(formattedHashtags) + ',' + str(account.default)+'\n')
    userDoc.close()


def accountInfo(account):
    print("\nAccount " + account.username)
    print("Like Percentage: " + account.likePercentage)
    print("Comment Percentage: " + account.commentPercentage)
    print("Num Accounts to Interact: " + account.numInteractions)
    print("Hashtags Searches: " + str(account.hashtags))
    print("Default Value: " + str(account.default))
    

def operation():
    print('What Operation do you want to do?\nChange Default User (1)\nCreate New Account(2)\nPrint Users (3)')
    operationNum = input()
    while operationNum not in ['1','2','3']:
        print("Incorrect input:" + operationNum + "\n")
        print('What Operation do you want to do?\nChange Default User (1)\nCreate New Account(2)\nPrint Users (3)')
        operationNum = input()
    if operationNum == '1':
        accounts = parseUserDoc()
        selectedAccount = selectedDefaultAccount = selectDefaultUser(accounts)
        writeUserDoc(accounts)
        accountInfo(selectedAccount)
    elif operationNum == '2':
        createFollowBotAccount()
        accounts = parseUserDoc()
        selectedAccount = selectDefaultUser(accounts)
        writeUserDoc(accounts)
        accountInfo(selectedAccount)
    else:
        accounts = parseUserDoc()
        for account in accounts:
            accountInfo(account)
            print()

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

if __name__ == "__main__":
    print('Instagram Quick Follow')
    if not path.exists("./bot_docs/accountInfo.txt"):
        createFollowBotAccount()
        accounts = parseUserDoc()
    else:
        accounts = parseUserDoc()
    operationVal = operation()
    print('Thanks to run default account info please use RunDefault.py')
    
