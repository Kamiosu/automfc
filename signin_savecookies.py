import pickle
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main(): 
    driver = initialize_driver()
    sign_in(driver)
    save_cookies(driver, 'cookies.pkl')

def initialize_driver():
    driver = webdriver.Chrome()
    driver.get('https://myfigurecollection.net/')
    click_sign_in(driver)
    return driver


def click_sign_in(driver):
    aall = driver.find_elements(By.CLASS_NAME, 'action')
    aall[0].click()


def sign_in(driver):
    USERNAME = 'kamiosu'
    PASSWORD = 'Will123Will123'

    username = driver.find_element(By.NAME, 'username')
    username.send_keys(USERNAME)

    password = driver.find_element(By.NAME, 'password')
    password.send_keys(PASSWORD)

    driver.find_element(By.XPATH, '//*[@id="wide"]/div/section/form/div/div[5]/div/input').click()

    
    
def save_cookies(driver, file_path):
    #Using selenium to get cookies and pickle to save them
    cookies = driver.get_cookies()
    with open(file_path, 'wb') as file:
        pickle.dump(cookies, file)

if __name__ == "__main__":
    main()
    