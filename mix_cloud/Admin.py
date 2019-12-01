from time import sleep, strftime
import random
import datetime
from os import path
from UserAccount import UserAccount
import uuid 

def createAccountType():
    print('What kind of bot account are you making? (Instagram or Mixcloud)')
    accountType = input()
    while accountType not in ['Mixcloud', 'Instagram']:
        print("Incorrect input: " + accountType)
        print('What kind of bot account are you making? (Instagram or Mixcloud)')
        operationNum = input()
    return accountType

def createEmail():
    print('What is your email?')
    email = input()
    return email

def createPassword():
    print('What is your password?')
    password = input()
    return password

def createOperation():
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

def createHashtags():
    print("What hashtag do you want to follow with? (type done to stop)")
    hashtags = []
    hashtag = input()
    while not hashtag == 'done':
        hashtags.append(hashtag)
        print("What hashtag do you want to follow with? (type done to stop)")
        print("Current hashtags: " + str(hashtags))
        hashtag = input()
    formattedHashtags = ''
    for hashtag in hashtags:
        formattedHashtags = formattedHashtags + '||' + hashtag
    return formattedHashtags

def createUsers():
    print("What user's followers do you want to follow with? (type done to stop)")
    users = []
    user = input()
    while not user == 'done':
        users.append(user)
        print("What user's followers do you want to follow with? (type done to stop)")
        print("Current users: " + str(users))
        user = input()
    formattedUsers = ''
    for user in users:
        formattedUsers = formattedUsers + '||' + user
    return formattedUsers

def createNumAccount():
    print('How many people do you want to follow with per hashtag or user? (It isn\'t good to go above 10 mixcloud can catch on!)')
    numInteractions = input()
    while not numInteractions.isdigit():
        print('Not an integer!')
        print('How many people do you want to interact per hashtag? (It isn\'t good to go above 10 mixcloud can catch on!)')
        numInteractions = input()
    return numInteractions

#User Doc Format: accountType, email, password, numInteractions, hashtags, users, default
def createFollowBotAccount():
    userDoc = open("./bot_docs/accountInfo.txt", "a")
    print('Welcome New Quick Follow User Create Account.')
    print('All this information is stored locally in a text file at this realtive file path ./account_lists/accountInfo.txt. \nKeep that file safe.')
    acccountType = createAccountType()
    email = createEmail()
    password = createPassword()
    formattedHashtags = createHashtags()
    formattedUsers = createUsers()
    numInteractions = createNumAccount()
    userDoc.write(acccountType + ',' + email + ',' + password + ',' + str(numInteractions) + ',' + formattedHashtags + ',' + formattedUsers + ',' + str(uuid.uuid1())+'\n')
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
        formattedUsers = ''
        for user in account.users:
            formattedUsers = formattedUsers + '||' + user
        print(str(account.accountType) + ',' + str(account.email) + ',' + str(account.password) + ',' + str(account.numInteractions) + ',' + str(formattedHashtags) + ',' + str(formattedUsers) + ',' + str(account.id)+'\n')
        userDoc.write(str(account.accountType) + ',' + str(account.email) + ',' + str(account.password) + ',' + str(account.numInteractions) + ',' + str(formattedHashtags) + ',' + str(formattedUsers) + ',' + str(account.id)+'\n')
    userDoc.close()

def accountInfo(account):
    print("\nAccount " + account.email)
    print("AccountType: " + account.accountType)
    print("Num Interactions: " + account.numInteractions)
    print("Hashtags Searches: " + str(account.hashtags))
    print('Follow Account: ' + str(account.users))
    print("ID Value: " + str(account.id))
    
def operation():
    print('What Operation do you want to do?\nCreate New Account(1)\nPrint Users (2)')
    operationNum = input()
    while operationNum not in ['1','2','3']:
        print("Incorrect input:" + operationNum + "\n")
        print('What Operation do you want to do?\nCreate New Account(1)\nPrint Users (2)')
        operationNum = input()
    if operationNum == '1':
        createFollowBotAccount()
        accounts = parseUserDoc()
        writeUserDoc(accounts)
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
        for val in split[4].split('||'):
            hashtags.append(val)
        users = []
        for val in split[5].split('||'):
            users.append(val)
        account = UserAccount(split[0],split[1],split[2],split[3],hashtags[1:], users[1:], split[6])
        accounts.append(account)
    accountDoc.close()
    return accounts

if __name__ == "__main__":
    print('Quick Follow')
    if not path.exists("./bot_docs/accountInfo.txt"):
        createFollowBotAccount()
        accounts = parseUserDoc()
    else:
        accounts = parseUserDoc()
    operationVal = operation()
    print('Thanks to run default account info please use follow_bot.py, followed by the desired account unique ID.')
    for account in accounts:
        print("Email:%s, UID:%s" %(account.email, account.id))
    
