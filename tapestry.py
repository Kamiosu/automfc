from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import pickle

import time

def main():
    driver = initialize_driver()
    driver.get('https://myfigurecollection.net/')
    load_cookies(driver, 'cookies.pkl')
    
    navigate_to_add_entry(driver)
    row1 = process_csv_data()
    add_entry(driver, row1)
    time.sleep(99999)

def initialize_driver():
    driver = webdriver.Chrome()
    return driver

def load_cookies(driver, file_path):
    with open(file_path, 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

# def click_sign_in(driver):
#     aall = driver.find_elements(By.CLASS_NAME, 'action')
#     aall[0].click()


# def sign_in(driver):
#     USERNAME = 'kamiosu'
#     PASSWORD = 'Will123Will123'

#     username = driver.find_element(By.NAME, 'username')
#     username.send_keys(USERNAME)

#     password = driver.find_element(By.NAME, 'password')
#     password.send_keys(PASSWORD)

#     driver.find_element(By.XPATH, '//*[@id="wide"]/div/section/form/div/div[5]/div/input').click()


def navigate_to_add_entry(driver):
    driver.find_element(By.XPATH, '//*[@id="menu"]/div[3]/a').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/h1/span[2]/span[2]/a[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/a').click()


def process_csv_data():
    df = pd.read_csv('data.csv')
    first_row = df.iloc[0]
    stripped_lower = [element.strip().lower() if isinstance(element, str) else element for element in first_row]
    return stripped_lower

def add_entry(driver, row):
    if(row[1] == 'goods'): 
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[1]/div[2]/a[2]').click()
        time.sleep(1)
        
    if(row[2] == 'on walls'): 
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[2]/div[2]/a[6]').click()
        time.sleep(1)

    if (row[3] == 'nsfw'):
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[3]/div[2]/a[2]').click()
        time.sleep(1)
        
    elif (row[3] == 'nsfw+'): 
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[1]/div/div[3]/div[2]/a[3]').click()
        time.sleep(1)
        
    if(row[4] != None):
        image = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[2]/div/div/div[2]/label')
        filepath = f"/Users/kamiosu/Downloads/MFC\ 2023/{row[4]}"
        # image.send_keys(filepath)



if __name__ == "__main__":
    main()
    




