from selenium import webdriver
import os
import time

os.chdir('C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\text-scraping')
file_path = os.getcwd()
driver = webdriver.Chrome(file_path+'/chromedriver.exe')

def log_in(usrnme, psswrd):
    
    driver.get("https://www.instagram.com")
    time.sleep(2)
    
    cookie_button = driver.find_element_by_xpath("//button[text()='Alle annehmen']")
    cookie_button.click()
    
    time.sleep(4)
    username_input = driver.find_element_by_css_selector("input[name='username']")
    password_input = driver.find_element_by_css_selector("input[name='password']")
    
    username_input.send_keys(usrnme)
    password_input.send_keys(psswrd)
    
    login_button =driver.find_element_by_xpath("//button[@type='submit']")
    login_button.click()
    
    time.sleep(5)
    
    save_login_info_button= driver.find_element_by_xpath("//button[text()='Jetzt nicht']")
    save_login_info_button.click()
    time.sleep(7)
    notification_button= driver.find_element_by_xpath("//button[text()='Jetzt nicht']")
    notification_button.click()

def insta_comment(usrnme, psswrd, urls):
    log_in(usrnme, psswrd)
    post_comments = []
    for link in urls:
        driver.get(link)
#        cookie_button = driver.find_element_by_xpath("//button[text()='Accept All']")
#        cookie_button.click()
        try:
            comment = driver.find_elements_by_xpath('//div[@class="C4VMK"]//span')[2].text
            post_comments.append(comment)
        except:
            print(link+" does not work")
        time.sleep(10)
    return post_comments

def write_to_txt_file(liste,file_name):
    
    textfile = open(file_name, "a+")
    for element in liste:
        textfile.write(element + "\n")
    textfile.close()
    
def read_from_file(file):   
    site_list=[]
    with open(file) as f:
        for line in f:
            li = [l.strip() for l in line.split('\n')]
            site_list.append(li[0])
        return site_list
    
post_links = read_from_file("websites-shaaz.txt")

full_text=insta_comment(MYUSERNAME, MYPASSWORD, post_links)
write_to_txt_file(full_text,"shaaz-text.txt")