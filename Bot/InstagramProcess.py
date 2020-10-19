from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import random
import datetime

class InstagramProcess:
    def __init__(self):
        self.username_input = 'username'
        self.password_input = 'password'
        self.follow_list = '/html/body/div[3]/div/div[2]/ul/div/li'
        self.follow_list_item = '/html/body/div[3]/div/div[2]/ul/div/li['
        self.first_picture = '/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]'
        self.next_button = '/html/body/div[4]/div[1]/div/div/a['
        self.follow_button = '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button'
        self.account_name = '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a'
        self.like_button = '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button'
        self.like_button_span = '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]'
        self.followed_list = []

    def parseDoc(self):
        filepath = './account-info/instagramFollowedList.txt'
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                self.followed_list.append(line.replace('\n',''))
                line = fp.readline()
        fp.close() 


    # Login Process
    def runLogin(self, webdriver, account):
        webdriver.get('https://www.%s.com/accounts/login' %(str.lower(account.accountType)))
        sleep(2)
        username = webdriver.find_element_by_name(self.username_input)
        username.send_keys(account.email)
        password = webdriver.find_element_by_name(self.password_input)
        password.send_keys(account.password)
        sleep(2)
        password.send_keys(Keys.RETURN)

    #not active
    def runFollowersFollow(self, webdriver, person, account, stopFlag):
        sleep(2)
        webdriver.get('https://www.%s.com/%s/followers/' %( str.lower(account.accountType), person))
        sleep(1)
        follow_list = webdriver.find_elements_by_xpath(self.follow_list)
        maxVal = len(follow_list)
        followDoc = open("./bot_docs/masterList.txt","a")
        for index in range(1,10):
            try:
                followButton = webdriver.find_element_by_xpath(self.follow_list_item +str(index)+']/div/div[3]/button')
                accountName = webdriver.find_element_by_xpath(self.follow_list_item +str(index)+']/div/div[2]/div[1]/div/div/a')
                webdriver.execute_script("return arguments[0].scrollIntoView();", followButton)
                sleep(random.uniform(0,1))
                # if(followButton.text=='Follow' and accountName.text not in clickedList.split(',')[0]):
                #     followButton.click()
                #     followDoc.write(accountName.text + ', ' + accountName.get_attribute("href") + datetime.today().strftime('%Y-%m-%d') + '\n')
            except:
                print("no follow button: " + self.follow_list_item +str(index)+']/div/div[3]/button')
        followDoc.close()

    def runHashtagFollow(self, webdriver, hashtag, account, stopFlag):
        sleep(2)
        webdriver.get('https://www.%s.com/explore/tags/%s/' %(str.lower(account.accountType),hashtag))
        firstPicture = webdriver.find_element_by_xpath(self.first_picture)
        firstPicture.click()
        sleep(1)
        val = 1
        likeCount = 0
        file_object = open('./account-info/instagramFollowedList.txt', 'a')
        while(likeCount < int(account.numInteractions)):
            if(random.randint(0,100) > 10 and stopFlag):
                stopFlag = self.hashtagFollow(webdriver, file_object)
                likeCount += 1
            self.hashtagLike(webdriver)
            # hashtagComment(selectedAccount.commentPercentage)
            nextButton = webdriver.find_element_by_xpath(self.next_button +str(val)+']')
            nextButton.click()
            val = 2

        # followDoc.close()
        return stopFlag

# needs to check if account has been followed before
    def hashtagFollow(self, webdriver, file_object):
        sleep(random.uniform(.5,1))
        followButton = webdriver.find_element_by_xpath(self.follow_button)
        accountName = webdriver.find_element_by_xpath(self.account_name)
        # if(followButton.text=='Follow' and accountName.text not in clickedList):
        if(followButton.text=='Follow'): 
            followButton.click()
            file_object.write(accountName.text+'\n')
        sleep(random.uniform(.5,2))
        if(followButton.text=='Follow'):
            return False
        return True

    def hashtagLike(self, webdriver):
        sleep(random.uniform(.5,1))
        likeButtonSpan = webdriver.find_element_by_xpath(self.like_button_span)
        likeButton = webdriver.find_element_by_xpath(self.like_button)
        if('outline' in likeButtonSpan.get_attribute("class")):
            likeButton.click()

    #not active
    def hashtagComment(self, commentPercentage):
        sleep(random.uniform(.5,1))
        commentButton = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button')
        if(random.randint(0,100)<int(commentPercentage)):
            commentInput = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')
            commentInput.send_keys('THAT LOOKS AMAZIN!!')
            postButton = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button')
            postButton.click()