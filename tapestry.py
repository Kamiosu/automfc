from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd
import json
import pickle
import time

def main():
    driver = initialize_driver()
    driver.get('https://myfigurecollection.net/')
    load_cookies(driver, 'cookies.pkl')
    time.sleep(1)
    navigate_to_add_entry(driver)
    entry1 = process_data()[0] #Only using the first entry for now
    add_entry(driver, entry1)   #Add the entry
    time.sleep(99999)

def initialize_driver():
    driver = webdriver.Chrome()
    return driver

def load_cookies(driver, file_path):
    with open(file_path, 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

def navigate_to_add_entry(driver):
    driver.find_element(By.XPATH, '//*[@id="menu"]/div[3]/a').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/h1/span[2]/span[2]/a[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/a').click()

def clean_up_dict(d):
    cleaned_dict = {}
    for k, v in d.items():
        if isinstance(v, str):
            cleaned_dict[k] = v.strip().lower()
        elif isinstance(v, list):
            cleaned_dict[k] = [s.strip().lower() for s in v if isinstance(s, str)]
        else:
            cleaned_dict[k] = v
    return cleaned_dict

def process_data():
    with open('data.json') as f:
        data = json.load(f)

    cleaned_data = [clean_up_dict(d) for d in data]
    return cleaned_data

def scrollby(driver, x, y):
    ActionChains(driver)\
        .scroll_by_amount(x,y)\
        .perform()

def pickentry(driver, entry, key):
    if(len(entry[key]) != 0): 
        for i in entry[key]:
            #================= Fill in the form with the id of the entry =================
            driver.find_element(By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/div/input').send_keys(i)
            #================= Click the search button =================
            driver.find_element(By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/input[2]').click()
            #for each entry in the list, enter into form, press search button, and select it when it comes up in the list
            #results are in a div with class "results", children have class "result"
            time.sleep(3) #This might take longe to load, how to make it wait until it's loaded?
            driver.find_element(By.XPATH,'//*[@id="window"]/div/div/form/div[2]/div[2]/div[2]/a').click()
            print("working")
            time.sleep(1)
    else: pass
            
def add_entry(driver, entry):
    # ============== Enter the root entry ==============
    if(entry['root'] == 'goods'): 
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[1]/div[2]/a[2]').click()
        time.sleep(1)
    
    # ============== Enter the category ==============
    if(entry['category'] == 'on walls'): 
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[2]/div[2]/a[6]').click()
        time.sleep(1)

    # ============== Enter the content level ==============
    if (entry['content_level'] == 'nsfw'):
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[3]/div[2]/a[2]').click()
        time.sleep(1)
        
    elif (entry['content_level'] == 'nsfw+'): 
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[3]/div[2]/a[3]').click()
        time.sleep(1)
    
    #Scroll to view next section of form
    scrollby(driver, 0, 500)
        
    time.sleep(1)
        
    if(entry['image_name'] != ""):
        pickimage = driver.find_element(By.XPATH, '//*[@id="fl-picture"]')
        filepath = f"/Users/kamiosu/Documents/PythonProjects/automfc/images/{entry['image_name']}"
        pickimage.send_keys(filepath)
    
    scrollby(driver, 0, 400)
    try:
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[3]/div/div[1]/div[2]/div[2]/a').click()
        time.sleep(2)
        # ============== Pick the orgins  ==============
        pickentry(driver, entry, 'origins')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[1]').click() #Go to character section
        # ============== Pick the characters  ==============
        pickentry(driver, entry, 'characters') 
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to companies section
        # ============== Pick the companies  ==============
        pickentry(driver, entry, 'companies')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to artists section
        # ============== Pick the artists  ==============
    except Exception as e:
        print(e)
    
    
    
if __name__ == "__main__":
    main()
    




