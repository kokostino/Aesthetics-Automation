from selenium import webdriver
import os
import time

file_path = os.getcwd()
driver = webdriver.Chrome(file_path+'/chromedriver.exe')

def log_in(usrnme, psswrd):
    
    driver.get("https://www.instagram.com")
    time.sleep(2)
    # cookie 
    cookie_button = driver.find_element_by_xpath("//button[text()='Alle annehmen']")
    cookie_button.click()
    
    time.sleep(4)
    username_input = driver.find_element_by_css_selector("input[name='username']")
    password_input = driver.find_element_by_css_selector("input[name='password']")
    
    username_input.send_keys(usrnme)
    password_input.send_keys(psswrd)
    
    login_button =driver.find_element_by_xpath("//button[@type='submit']")
    login_button.click()
    
    time.sleep(3)
    # not now
    save_login_info_button= driver.find_element_by_xpath("//button[text()='Jetzt nicht']")
    save_login_info_button.click()
    time.sleep(4)
    notification_button= driver.find_element_by_xpath("//button[text()='Jetzt nicht']")
    notification_button.click()
    
def get_all_posts(username, anzahl):
    
    driver.get("https://www.instagram.com/"+username+"/?hl=en")
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < anzahl:
        links = [a.get_attribute('href') for a in driver.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll_down)
        time.sleep(6)
    else:
        return post_links[:anzahl]
    
def insta_comment(urls):
    
    post_comments = []
    for link in urls:
        driver.get(link)
        comment = driver.find_elements_by_xpath('//div[@class="C4VMK"]//span')[2].text
        post_comments.append(comment)
        time.sleep(7)
    return post_comments

def write_to_txt_file(liste,file_name):
    
    textfile = open(file_name, "w+")
    for element in liste:
        textfile.write(element + "\n")
    textfile.close()
    
log_in(MEIN_ACCOUNT,MEIN_PASSWORT)
time.sleep(2)
post_links=get_all_posts(USERSEITE, 700)
time.sleep(5)
full_text=insta_comment(post_links[:5])
write_to_txt_file(full_text,FILENAME)
