from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint

chromedriver_path = 'C:/Users/plagambino/Documents/Other_Work/Bot/chromedriver.exe' 
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

sleep(1)

# Login Process
def login():
    webdriver.get('https://www.mixcloud.com')
    sleep(4)
    login_button_1 = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[3]/div/div/header/div/div[3]/div/span[1]')
    login_button_1.click()
    username = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[1]/div/input')
    username.send_keys('redshirtsmusicexperience@gmail.com')
    password = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[1]/span[16]/div/div[2]/div/div/div/form/div[2]/div/input')
    password.send_keys('ket6D91gip')
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
    # print(follow_list)
    for val in range(3,max_val):
        try:
            follow_button = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
            follow_button.click()
            print("Clicked: " + '//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
        except:
            print("no follow button: " + '//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
        # print(follow_button)
        sleep(1)
# Follow Block
# //*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li[1]

def followersFollow(person):
    sleep(4)
    webdriver.get('https://www.mixcloud.com/DjHIDEKI/followers/')
    follow_list = webdriver.find_elements_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li')
    max_val = len(follow_list)
    index = 1
    scroll_down_val = 0
    follow_doc = open("followList.txt","a")
    while(scroll_down_val < 100):
        like_num = randint(10,20)
        like_count = 0
        for val in range(index,max_val):
            if(like_count == like_num):
                sleep(randint(600,1000))
                like_count = 0
            # webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
            try:
                # Attempt to click follow button
                follow_button = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li['+str(val)+']/button')
                webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)
                webdriver.execute_script("window.scrollBy(0, -" + str(randint(170,200)) + ")")
                sleep(randint(1,6))
                follow_button.click()
                webdriver.execute_script("window.scrollBy(0, -" + str(randint(10,20)) + ")")
                name = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li['+str(val)+']/span/b/span/a')
                follow_doc.write(name.get_attribute("href")+ "," + name.text + '\n')
                like_count = like_count + 1
            except:
                print("no follow button: " + '//*[@id="react-root"]/div/section/div[4]/div/div/div[1]/div/div/section/div[1]/div[2]/div[2]/section/div/ul/li['+str(val)+']/button')
            webdriver.execute_script("window.scrollBy(0, 200)")
        sleep(3)
        follow_list = webdriver.find_elements_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li')
        index = max_val
        max_val = len(follow_list)
        print(len(follow_list))
        scroll_down_val += 1
    follow_doc.close()

def scroll():
    webdriver.get('https://www.mixcloud.com/DjHIDEKI/followers/')
    follow_button = webdriver.find_element_by_xpath('//*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li[15]/button')
    sleep(1)
    webdriver.execute_script("return arguments[0].scrollIntoView();", follow_button)

if __name__ == "__main__":
    print('Mixcloud Follow Run')
    login()
    followersFollow('house')
    

# notnow = webdriver.find_element_by_css_selector('body > div:nth-child(13) > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
# notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications
# //*[@id="react-root"]/div/section/div[4]/div/div/div/div/div[4]/main/div[1]/div[2]/ul/li[15]/button/span