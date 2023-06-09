# Standard library imports
import json
import pickle
import time

# External library imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotSelectableException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

# Local imports
import scraperGOT
from scraperGOT import getchu_urls
import melonTapestry
from melonTapestry import melon_urls
import melonDoujin
from melonDoujin import melon_urls
import melonUribou
from melonUribou import melon_urls
# from scrape_entry.ArtistNotFoundException import ArtistNotFoundException
# from scrape_entry.CompanyNotFoundException import CompanyNotFoundException

# Constants
URL = 'https://myfigurecollection.net/figure'
COOKIES = 'cookies.pkl'
IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"
XPATHS = {}
RUN = {
    'standard': '1',
    'limited': '2',
    'exclusive': '3',
    'limited+exclusive': '4',
    'prize': '5',
    'unknown': '7',  # idk why this is even 7
}

'''
============== VALID TYPES ==============
one: adds an entry with only one url
uribou: adds a uribou tapestry entry
'''
TYPE = "one"
COMPANY = "Getchu"
# COMPANY = "Melonbooks"


# ========================================

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
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div[1]/h1/span[2]/span[2]/a[1]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/a').click()

# ============== Extract, Clean return data ==============


def clean_up_dict(d):
    cleaned_dict = {}
    for k, v in d.items():
        if isinstance(v, str):
            cleaned_dict[k] = v.strip().lower()
        elif isinstance(v, list):
            cleaned_dict[k] = [s.strip().lower()
                               for s in v if isinstance(s, str)]
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
        .scroll_by_amount(x, y)\
        .perform()


def section_category(driver, entry):
    # ============== Enter the root entry ==============
    if(entry['root'] == 'figure'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[1]/div[2]/a[1]').click()
        time.sleep(1)
    elif(entry['root'] == 'goods'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[1]/div[2]/a[2]').click()
        time.sleep(1)
    elif(entry['root'] == 'media'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[1]/div[2]/a[3]').click()
        time.sleep(1)
    # ============== Enter the category ==============
    if(entry['category'] == 'on walls'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[2]/div[2]/a[6]').click()
        time.sleep(1)
    if(entry['category'] == 'linens'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[2]/div[2]/a[2]').click()
        time.sleep(1)
    elif(entry['category'] == 'books'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[2]/div[2]/a[1]').click()
        time.sleep(1)

    # ============== Enter the content level ==============
    if (entry['content_level'] == 'nsfw'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[3]/div[2]/a[2]').click()
        time.sleep(1)

    elif (entry['content_level'] == 'nsfw+'):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[1]/section/div/div[3]/div[2]/a[3]').click()
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
                # ================= Fill in the form with the id of the entry =================
                driver.find_element(
                    By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/div/input').send_keys(i)
                # ================= Click the search button =================
                driver.find_element(
                    By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/input[2]').click()
                # for each entry in the list, enter into form, press search button, and select it when it comes up in the list
                # results are in a div with class "results", children have class "result"
                # time.sleep(2) #This might take longe to load, how to make it wait until it's loaded?
                time.sleep(2)
                wait_for_element(
                    driver, '//*[@id="window"]/div/div/form/div[2]/div[2]/div[2]/a')

                driver.find_element(
                    By.XPATH, '//*[@id="window"]/div/div/form/div[2]/div[2]/div[2]/a').click()
                print("working")
                time.sleep(1)
            except Exception as e:
                print(e)
                pass

            finally:
                driver.find_element(
                    By.XPATH, '//*[@id="window"]/div/div/form/div[1]/div[2]/div[1]/div/input').clear()

    else:
        pass


def section_entries(driver, entry):
    try:
        # ============== Find origins button ==============
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[3]/section/div/div[1]/div[2]/div[2]/a').click()
        time.sleep(1)
        # ============== Pick the orgins  ==============
        if(len(entry['origins']) != 0):
            pickentry(driver, entry, 'origins')
        # Go to character section
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[1]').click()
        time.sleep(1)
        # ============== Pick the characters  ==============
        if(len(entry['characters']) != 0):
            pickentry(driver, entry, 'characters')
        # Go to companies section
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click()
        time.sleep(1)

        # ============== Pick the companies  ==============
        if (len(entry['companies']) != 0):
            pickentry(driver, entry, 'companies')
        # Go to artists section
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click()
        time.sleep(1)

        # ============== Pick the artists  ==============
        if (len(entry['artists']) != 0):
            pickentry(driver, entry, 'artists')
        # Go to classifications section
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click()
        time.sleep(1)

        # ================= Pick the classifications =================
        if (len(entry['classifications']) != 0):
            pickentry(driver, entry, 'classifications')
        # Go to materials section
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click()
        time.sleep(1)

        # ================= Pick the Materials =================
        if (len(entry['materials']) != 0):
            pickentry(driver, entry, 'materials')
        # Go to events section
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[2]').click()
        time.sleep(1)

        # ================= Pick the Events =================
        if (entry['events'] != None):
            pickentry(driver, entry, 'events')
        time.sleep(1)

        # Exit the form
        driver.find_element(
            By.XPATH, '//*[@id="window"]/div/h2/nav/a[4]').click()  # CLOSE
    except Exception as e:
        print(e)
        pass


def refine(driver, entry):
    # =========== select type for Company, set to appropriate tag =================
    company = Select(driver.find_element(By.XPATH, '//*[@id="main"]/div/div/form/div[3]/section/div/div[3]/div[2]/div[1]/div/div[2]/select'))
    if (company != None): 
        if (entry['root'] == 'media'): 
            company.select_by_visible_text('Circle')    
    # =========== select type for artist, set to appropriate tag =================
    artist = Select(driver.find_element(
        By.XPATH, '//*[@id="main"]/div/div/form/div[3]/section/div/div[4]/div[2]/div[1]/div/div[2]/select'))
    if(artist != None):
        if (entry['root'] == 'goods'):
            artist.select_by_visible_text('Illustrator')
        elif (entry['root'] == 'media'):
            artist.select_by_visible_text('Mangaka')

    # =========== Enter the classification id if it exists =================
    if(entry['classifications_id'] != None):
        hash_id = driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[3]/section/div/div[5]/div[2]/div[1]/div/div[2]/input')
        hash_id.send_keys(entry['classifications_id'])


def section_releases(driver, entry):
    # ================= ADD A RELEASE DATE + RELEVANT INFO =================
    driver.find_element(
        By.XPATH, '//*[@id="main"]/div/div/form/div[4]/section/div/div[1]/div/div[2]/a').click()
    time.sleep(1)
    scroll_by(driver, 0, 50)
    if((entry['category'] == 'books' and entry['events'] != None) or TYPE == "uribou"):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[4]/section/div/div[1]/div/div[2]/a').click()
        scroll_by(driver, 0, 50)
    if(TYPE == "uribou"):
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[4]/section/div/div[1]/div/div[2]/a').click()
        scroll_by(driver, 0, 80)
    
    
    time.sleep(1)
    # ================= Select the release year =================
    year = Select(driver.find_element(By.NAME, 'releaseYears[]'))
    if(entry['release_year'] != None):
        year.select_by_visible_text(entry['release_year'])
    # ================= Select the release month =================
    month = Select(driver.find_element(By.NAME, 'releaseMonths[]'))
    if(entry['release_month'] != None):
        if(len(entry['release_month']) == 1):
            month.select_by_visible_text('0' + entry['release_month'])
        else:
            month.select_by_visible_text(entry['release_month'])
    # ================= Select the release day =================
    day = Select(driver.find_element(By.NAME, 'releaseDays[]'))
    if(entry['release_day'] != None):
        if(len(entry['release_day']) == 1):
            day.select_by_visible_text('0' + entry['release_day'])
        else:
            day.select_by_visible_text(entry['release_day'])
    # ================= Select the run type =================
    run = Select(driver.find_element(By.NAME, 'releaseRunIds[]'))
    if(entry['run'] != None):
        run.select_by_value(RUN[entry['run']])
    # ================= Enter the price =================
    if(entry['notaxprice'] != None):
        driver.find_element(By.NAME, 'releasePrices[]').send_keys(
            entry['notaxprice'])
    # ================= Enter the barcode=================
    if(entry['barcode'] != None):
        driver.find_element(By.NAME, 'releaseBarcodes[]').send_keys(
            entry['barcode'])
    # ================= Enter the size =================
    if(entry['size'] != None):
        driver.find_element(By.NAME, 'releaseSizes[]').send_keys(entry['size'].upper())
      

    # ================= IF THERE IS AN EVENT FOR DOUJIN, ADD ANOTHER RELEASE FOR THAT EVENT =================
     # ================= Select the release year =================
    if((entry['category'] == 'books' and entry['events'] != None) or TYPE == "uribou"):
        year2 = Select(driver.find_elements(By.NAME, 'releaseYears[]')[1])
        if(entry['release_year'] != None):
            year2.select_by_visible_text(entry['release_year'])
        # ================= Select the release month =================
        month2 = Select(driver.find_elements(By.NAME, 'releaseMonths[]')[1])
        if(entry['release_month'] != None):
            if(len(entry['release_month']) == 1):
                month2.select_by_visible_text('0' + entry['release_month'])
            else:
                month2.select_by_visible_text(entry['release_month'])
        # ================= Select the release day =================
        day2 = Select(driver.find_elements(By.NAME, 'releaseDays[]')[1])
        if(entry['release_day'] != None):
            if(len(entry['release_day']) == 1):
                day2.select_by_visible_text('0' + entry['release_day'])
            else:
                day2.select_by_visible_text(entry['release_day'])
        # ================= Select the run type =================
        run2 = Select(driver.find_elements(By.NAME, 'releaseRunIds[]')[1])
        if(entry['run'] != None):
            run2.select_by_value(RUN['exclusive'])
        # ================= Enter the price =================
        if(entry['notaxprice'] != None):
            if(TYPE == "uribou"):
                driver.find_elements(By.NAME, 'releasePrices[]')[
                1].send_keys(6000)
            else: 
                driver.find_elements(By.NAME, 'releasePrices[]')[
                    1].send_keys(entry['notaxprice'])
        # ================= Enter the barcode=================
        if(entry['barcode'] != None):
            driver.find_elements(By.NAME, 'releaseBarcodes[]')[
                1].send_keys(entry['barcode'])
        # ================= Enter the size =================
        if(entry['size'] != None):
            if(TYPE == "uribou"):
                driver.find_elements(By.NAME, 'releaseSizes[]')[
                1].send_keys("B1")
            else:
                driver.find_elements(By.NAME, 'releaseSizes[]')[
                1].send_keys(entry['size'].upper())
        # ================= Enter additional info =================
        if(entry['additional_info'] != None):
            driver.find_elements(By.NAME, 'releaseEvents[]')[
                1].send_keys(entry['additional_info'])
    
    if(TYPE == "uribou"):
        scroll_by(driver, 0, 900) 
        time.sleep(1)
        year2 = Select(driver.find_elements(By.NAME, 'releaseYears[]')[2])
        if(entry['release_year'] != None):
            year2.select_by_visible_text(entry['release_year'])
        # ================= Select the release month =================
        month2 = Select(driver.find_elements(By.NAME, 'releaseMonths[]')[2])
        if(entry['release_month'] != None):
            if(len(entry['release_month']) == 1):
                month2.select_by_visible_text('0' + entry['release_month'])
            else:
                month2.select_by_visible_text(entry['release_month'])
        # ================= Select the release day =================
        day2 = Select(driver.find_elements(By.NAME, 'releaseDays[]')[2])
        if(entry['release_day'] != None):
            if(len(entry['release_day']) == 1):
                day2.select_by_visible_text('0' + entry['release_day'])
            else:
                day2.select_by_visible_text(entry['release_day'])
        # ================= Select the run type =================
        run2 = Select(driver.find_elements(By.NAME, 'releaseRunIds[]')[2])
        if(entry['run'] != None):
            run2.select_by_value(RUN['exclusive'])
        # ================= Enter the price =================
        if(entry['notaxprice'] != None):
            if(TYPE == "uribou"):
                driver.find_elements(By.NAME, 'releasePrices[]')[
                2].send_keys(11000)
            else: 
                driver.find_elements(By.NAME, 'releasePrices[]')[
                2].send_keys(entry['notaxprice'])
        # ================= Enter the barcode=================
        if(entry['barcode'] != None):
            driver.find_elements(By.NAME, 'releaseBarcodes[]')[
                2].send_keys(entry['barcode'])
        # ================= Enter the size =================
        if(entry['size'] != None):
            driver.find_elements(By.NAME, 'releaseSizes[]')[
                2].send_keys('B0')


def section_furtherinfo(driver, entry):
    # ================= Enter the title =================
    if(entry['title'] != None):
        driver.find_element(By.NAME, 'title').send_keys(entry['title'])
        time.sleep(1)
        # Normalize the title
        driver.find_element(
            By.XPATH, '//*[@id="main"]/div/div/form/div[5]/section/div/div[1]/div[2]/div/a').click()
        time.sleep(.5)
    # ================= Enter the original title =================
    if(entry['original_title'] != None):
        driver.find_element(By.NAME, 'originalTitle').send_keys(
            entry['original_title'])

    # ================= Enter the Numbering ===================
    if(entry['numbering'] != None):
        driver.find_element(By.NAME, 'numbering').send_keys(entry['numbering'])

    # ================= Enter the page number =================
    if (entry['pages'] != None):
        driver.find_element(By.NAME, 'countPages').send_keys(entry['pages'])

    # ================= Scroll to the last section and submit button =================
    time.sleep(1)
    if(entry['content_level'] == "nsfw" or entry['content_level'] == "nsfw+"):
        driver.find_element(By.XPATH, '//*[@id="rd-rating-3"]').click()

    scroll_by(driver, 0, 800)
    time.sleep(1)

    if(TYPE == "uribou"):
        uribou(driver, entry)
    elif(TYPE == "one"):
        oneURL(driver, entry)
    else:
        print("No TYPE specified")


def uribou(driver, entry):
    three_sizes = f'Product Page → [url={entry["links"][0]}]B2[/url] | [url={entry["links"][1]}]B1[/url] | [url={entry["links"][1]}]B0[/url]'
    driver.find_element(By.NAME, 'infoNote').send_keys(three_sizes)


def oneURL(driver, entry):
    onelink = f'[url={entry["links"][0]}]{COMPANY}[/url]'
    driver.find_element(By.NAME, 'infoNote').send_keys(onelink)


def submit_entry(driver):
    submit = driver.find_element(
        By.XPATH, '//*[@id="main"]/div/div/form/div[8]/section/div/div[3]/div/input[1]')
    submit.click()
    time.sleep(1)
    scroll_by(driver, 0, 1000)
    time.sleep(1)
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[
                         ElementNotVisibleException, ElementNotSelectableException])
    submit_thumbnail = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id='wide']/div/section/form/div/div[2]/div/input[2]")))
    # submit_thumbnail = driver.find_element(By.XPATH, '//*[@id="wide"]/div/section/form/div/div[2]/div/input[2]')
    submit_thumbnail.click()


def add_entry(driver, entry):
    try:
        section_category(driver, entry)
        selectPhoto(driver, entry)
        # Scroll to view next section of form
        scroll_by(driver, 0, 500)

        time.sleep(1)

        section_entries(driver, entry)

        scroll_by(driver, 0, 700)

        time.sleep(1)

        refine(driver, entry)

        scroll_by(driver, 0, 1000)

        time.sleep(2)

        section_releases(driver, entry)

        time.sleep(2)

        scroll_by(driver, 0, 600)

        time.sleep(2)

        section_furtherinfo(driver, entry)

        time.sleep(1.5)

        submit_entry(driver)

    except Exception as e:
        print(e)


def add_got_tapestry(driver):
    for i in range(len(getchu_urls)):
        if(getchu_urls[i] != ""):
            print(f'\nAdding entry {i+1}/{len(getchu_urls)}\n')
            driver.get(URL)
            scraperGOT.main(i)
            main_process(driver)


def add_melon_tapestry(driver):
    for i in range(len(melonTapestry.melon_urls)):
        if(melonTapestry.melon_urls[i] != ""):
            print(f'\nAdding entry {i+1}/{len(melonTapestry.melon_urls)}\n')
            driver.get(URL)
            melonTapestry.main(i)
            main_process(driver)


def add_melon_doujin(driver):
    for i in range(len(melonDoujin.melon_urls)):
        if(melonDoujin.melon_urls[i] != ""):
            print(f'\nAdding entry {i+1}/{len(melonDoujin.melon_urls)}\n')
            driver.get(URL)
            melonDoujin.main(i)
            main_process(driver)
            
def add_uribou_tapestry(driver):
    for i in range(len(melonUribou.melon_urls)):
        if(melonUribou.melon_urls[i] != ""):
            print(f'\nAdding entry {i+1}/{len(melonUribou.melon_urls)}\n')
            driver.get(URL)
            melonUribou.main(i)
            main_process(driver)

def main_process(driver):
    driver.get(URL)
    navigate_to_add_entry(driver)
    entry1 = process_data()[0]
    add_entry(driver, entry1)  # Add the entry
    time.sleep(3)
    print("Finished Adding Entry!")


def main():
    driver = initialize_driver()
    driver.get(URL)
    load_cookies(driver, COOKIES)
    time.sleep(1)

    add_got_tapestry(driver)
    # add_melon_tapestry(driver)
    # add_melon_doujin(driver)
    # add_uribou_tapestry(driver)


if __name__ == "__main__":
    main()
