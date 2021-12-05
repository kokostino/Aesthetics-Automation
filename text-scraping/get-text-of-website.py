from selenium import webdriver
import os
import time

file_path = os.getcwd()
driver = webdriver.Chrome(file_path+'/chromedriver.exe')

driver.get("https://www.instagram.com")
time.sleep(2)

cookie_button = driver.find_element_by_xpath("//button[text()='Alle annehmen']")
cookie_button.click()

time.sleep(4)
username_input = driver.find_element_by_css_selector("input[name='username']")
password_input = driver.find_element_by_css_selector("input[name='password']")
    
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORT)
    
login_button =driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()
    
time.sleep(3)
    
save_login_info_button= driver.find_element_by_xpath("//button[text()='Jetzt nicht']")
save_login_info_button.click()
time.sleep(4)
notification_button= driver.find_element_by_xpath("//button[text()='Jetzt nicht']")
notification_button.click()
time.sleep(7)

def insta_comment(urls):
    post_comments = []
    for link in urls:
        driver.get(link)
        try:
            comment = driver.find_elements_by_xpath('//div[@class="C4VMK"]//span')[2].text
            post_comments.append(comment)
        except:
            print(link+" does not work")
        time.sleep(10)
    return post_comments

def read_from_file(file):   
    site_list=[]
    with open(file) as f:
        for line in f:
            li = [l.strip() for l in line.split('\n')]
            site_list.append(li[0])
        return site_list

def write_to_txt_file(list,file_name):
    textfile = open(file_name, "a+", encoding="utf-8")
    for element in list:
        textfile.write(element + "\n")
    textfile.close()
    
post_links = read_from_file("websites-shaaz.txt")
full_text=insta_comment(post_links)
write_to_txt_file(full_text,'shaaz.txt')




import re
def write_to_txt_file_other(liste,file_name):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    textfile = open(file_name, "w+")
    for element in liste:
        textfile.write(emoji_pattern.sub(r'', element) + "\n")
    textfile.close()