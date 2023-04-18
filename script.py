# Standard library imports
import json
import pickle
import time

# External library imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
import scraper


# Constants
URL = 'https://myfigurecollection.net/'
COOKIES = 'cookies.pkl'
IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"
XPATHS = {}
RUN = { 
    'standard': '1',
    'limited': '2',
    'exclusive': '3',
    'limited+exclusive': '4',
    'prize': '5',
    'unknown': '7', #idk why this is even 7
    }
SIZE = { 
    'a0': 'A0',
    'a1': 'A1',
    'a2': 'A2',
    'a3': 'A3',
    'a4': 'A4',
    'a5': 'A5',
    'a6': 'A6',
    'b0': 'B0',
    'b1': 'B1',
    'b2': 'B2',
    'b3': 'B3',
    'b4': 'B4',
    'b5': 'B5',
    'b6': 'B6',
    'xs': 'XS',
    's': 'S',
    'm': 'M',
    'l': 'L',
    'xl': 'XL',
    }

'''
============== VALID TYPES ==============
one: adds an entry with only one url
uribou: adds a uribou tapestry entry
'''
TYPE = "one"
COMPANY = "GOT"


#========================================

def initialize_driver():
    driver = webdriver.Chrome()
    return driver

def load_cookies(driver, file_path):
    with open(file_path, 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

def wait_for_element(driver, xpath, timeout=10):
    """
    Wait for an element to be loaded and return it.
    """
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def navigate_to_add_entry(driver):
    driver.find_element(By.XPATH, '//*[@id="menu"]/div[3]/a').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/h1/span[2]/span[2]/a[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/a').click()

# ============== Extract, Clean return data ==============
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

# ============== ========================== ==============

def scroll_by(driver, x, y):
    ActionChains(driver)\
        .scroll_by_amount(x,y)\
        .perform()

def section_category(driver, entry):
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

def selectPhoto(driver, entry):
    if(entry['image_name'] != ""):
        pickimage = driver.find_element(By.XPATH, '//*[@id="fl-picture"]')
        filepath = f"{IMAGES_PATH}{entry['image_name']}"
        pickimage.send_keys(filepath)

def pickentry(driver, entry, key):
    if(len(entry[key]) != 0): 
        for i in entry[key]:
            try:
                #================= Fill in the form with the id of the entry =================
                driver.find_element(By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/div/input').send_keys(i)
                #================= Click the search button =================
                driver.find_element(By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/input[2]').click()
                #for each entry in the list, enter into form, press search button, and select it when it comes up in the list
                #results are in a div with class "results", children have class "result"
                #time.sleep(2) #This might take longe to load, how to make it wait until it's loaded?
                time.sleep(2)
                wait_for_element(driver, '//*[@id="window"]/div/div/form/div[2]/div[2]/div[2]/a')
                
                driver.find_element(By.XPATH,'//*[@id="window"]/div/div/form/div[2]/div[2]/div[2]/a').click()
                print("working")
                time.sleep(1)
            except Exception as e:
                print(e)
                pass
            
            finally: 
                driver.find_element(By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/div/input').clear()
                
    else: pass           
            
def section_entries(driver, entry):
    try: 
        # ============== Find origins button ==============
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[3]/div/div[1]/div[2]/div[2]/a').click()
        time.sleep(1)
        # ============== Pick the orgins  ==============
        if(len(entry['origins']) != 0):
            pickentry(driver, entry, 'origins')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[1]').click() #Go to character section
        time.sleep(1)
        # ============== Pick the characters  ==============
        if(len(entry['characters']) != 0):
            pickentry(driver, entry, 'characters') 
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to companies section
        time.sleep(1)
        
        # ============== Pick the companies  ==============
        if (len(entry['companies']) != 0):
            pickentry(driver, entry, 'companies')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to artists section
        time.sleep(1)
        
        # ============== Pick the artists  ==============
        if (len(entry['artists']) != 0):
            pickentry(driver, entry, 'artists')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to classifications section
        time.sleep(1)
        
        #================= Pick the classifications =================
        if (len(entry['classifications']) != 0):
            pickentry(driver, entry, 'classifications')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to materials section
        time.sleep(1)
        
        #================= Pick the Materials =================
        if (len(entry['materials']) != 0):
            pickentry(driver, entry, 'materials')
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click() #Go to events section
        time.sleep(1)
        
        #================= Pick the Events =================
        if (len(entry['events']) != 0):
            pickentry(driver, entry, 'events')
        time.sleep(1)
            
        #Exit the form 
        driver.find_element(By.XPATH, '//*[@id="window"]/div/h2/nav/a[4]').click() #CLOSE
    except Exception as e:
        print(e)
        pass      

def section_releases(driver, entry):
    #================= ADD A RELEASE DATE + RELEVANT INFO =================
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/section[4]/div/div[1]/div/div[2]/a').click()
        time.sleep(1)
        #================= Select the release year =================
        year = Select(driver.find_element(By.NAME, 'releaseYears[]'))
        if(entry['release_year'] != ""):
            year.select_by_value(entry['release_year'])
        #================= Select the release month =================
        month = Select(driver.find_element(By.NAME, 'releaseMonths[]'))
        if(entry['release_month'] != ""):
            month.select_by_value(entry['release_month'])
        #================= Select the release day =================
        day = Select(driver.find_element(By.NAME, 'releaseDays[]'))
        if(entry['release_day'] != ""):
            day.select_by_value(entry['release_day'])
        #================= Select the run type =================
        run = Select(driver.find_element(By.NAME, 'releaseRunIds[]'))
        if(entry['run'] != ""):
            run.select_by_value(RUN[entry['run']])
        #================= Enter the price =================
        if(entry['notaxprice'] != None):  
            driver.find_element(By.NAME, 'releasePrices[]').send_keys(entry['notaxprice'])
        #================= Enter the barcode=================
        if(entry['barcode'] != ""):
            driver.find_element(By.NAME, 'releaseBarcodes[]').send_keys(entry['barcode'])
        #================= Enter the size =================
        if(entry['size'] != ""):
            driver.find_element(By.NAME, 'releaseSizes[]').send_keys(SIZE[entry['size']])
        #================= Enter additional info =================
        if(entry['additional_info'] != ""):
            driver.find_element(By.NAME, 'releaseEvents[]').send_keys(entry['additional_info'])

def section_furtherinfo(driver, entry):
    #OTHER STUFF NOT YET DONE
    #================= Scroll to the last section and submit button =================
    scroll_by(driver, 0, 700)
    time.sleep(1)
    if(entry['content_level'] == "nsfw" or entry['content_level'] == "nsfw+"):
        driver.find_element(By.XPATH, '//*[@id="rd-rating-3"]').click()

    if(TYPE == "uribou"):    
        uribou(driver, entry)
    elif(TYPE == "one"): 
        oneURL(driver, entry)
    else: print("No TYPE specified")
    
def uribou(driver, entry):
    three_sizes = f'Product Page → [url={entry["links"][0]}]B2[/url] | [url={entry["links"][1]}]B1[/url] | [url={entry["links"][2]}]B0[/url]' 
    driver.find_element(By.NAME, 'information').send_keys(three_sizes)
    
def oneURL(driver, entry): 
    onelink = f'[url={entry["links"][0]}]{COMPANY}[/url]'
    driver.find_element(By.NAME, 'information').send_keys(onelink)
    

def add_entry(driver, entry):
    try:
        section_category(driver, entry) 
        
        #Scroll to view next section of form
        scroll_by(driver, 0, 500)
        
        selectPhoto(driver, entry)
            
        time.sleep(1)
        
        scroll_by(driver, 0, 400)
        
        time.sleep(1)
        
        section_entries(driver, entry)
        
        scroll_by(driver, 0, 2000)
        
        time.sleep(1)
        
        section_releases(driver, entry)
        
        time.sleep(1)
        
        scroll_by(driver, 0, 900)
        
        time.sleep(1)
        
        section_furtherinfo(driver, entry)
        
        
    except Exception as e:
        print(e)
    
    
def main():
    scraper.main()
    time.sleep(2)
    driver = initialize_driver()
    driver.get(URL)
    load_cookies(driver, COOKIES)
    time.sleep(1)
    navigate_to_add_entry(driver)
    entry1 = process_data()[0] #Only using the first entry for now
    add_entry(driver, entry1)   #Add the entry
    time.sleep(99999)
   
    
if __name__ == "__main__":
    main()
    




