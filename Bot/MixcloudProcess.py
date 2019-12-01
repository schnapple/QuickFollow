from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
import random
import datetime

class MixcloudProcess:
    def __init__(self):
        self.login_button = '//*[@id="react-root"]/div/section/div[3]/div/div/header/div/div[3]/div/span[1]'
        self.email_input = '//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[1]/div/input'
        self.password_input = '//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[2]/div/input'
        self.follow_list = '/html/body/div[1]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li'
        self.follow_list_item = '/html/body/div[1]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li['

    def runLogin(self, webdriver, account):
        webdriver.get('https://www.%s.com' %(str.lower(account.accountType)))
        sleep(2)
        login_button = webdriver.find_element_by_xpath(self.login_button)
        login_button.click()
        email = webdriver.find_element_by_xpath(self.email_input)
        email.send_keys(account.email)
        password = webdriver.find_element_by_xpath(self.password_input)
        password.send_keys(account.password)
        sleep(2)
        password.send_keys(Keys.RETURN)

    def runFollowersFollow(self, webdriver, person, account, stopFlag):
        sleep(2)      
        webdriver.get('https://www.%s.com/%s/followers/' %( str.lower(account.accountType), person))
        follow_list = webdriver.find_elements_by_xpath(self.follow_list)
        index = 1
        like_count = 0
        while(like_count < int(account.numInteractions)):
            for val in range(index,len(follow_list)):
                if random.randint(0,5) > 2 and stopFlag:
                    stopFlag = self.clickFollowButton(webdriver, val, stopFlag)
                    webdriver.execute_script("window.scrollBy(0, 200)")
                    if(like_count >= int(account.numInteractions)):
                        break
            index = len(follow_list)
            follow_list = webdriver.find_elements_by_xpath(self.follow_list)
        return stopFlag

    def clickFollowButton(self, webdriver, val, stopFlag):
        try:
            follow_button = webdriver.find_element_by_xpath(self.follow_list_item +str(val)+ ']/button')
            webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)
            webdriver.execute_script("window.scrollBy(0, -" + str(random.randint(150,200)) + ")")
            sleep(random.uniform(.5,6))
            follow_button.click()
            sleep(random.uniform(.5,2))
            follow_text = webdriver.find_element_by_xpath(self.follow_list_item +str(val)+ ']/button/span')
            print(follow_text.text)
            if follow_text.text == 'Follow':
                print('Hit Max Follows Stopping')
                stopFlag = False
            webdriver.execute_script("window.scrollBy(0, -" + str(random.randint(10,50)) + ")")
            name = webdriver.find_element_by_xpath(self.follow_list_item +str(val)+ ']/span/b/span/a')
            like_count = like_count + 1
        except:
            print("Follow Button Not Present: "+str(val))
        return stopFlag

    #Not active
    def runHashtagFollow(self, hashtag, clickedList, selectedAccount):
        sleep(4)
        search_bar = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/header/div/div[2]/input')
        search_bar.click()
        search_bar.send_keys(hashtag)
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
        return True