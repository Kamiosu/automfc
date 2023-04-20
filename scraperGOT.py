from bs4 import BeautifulSoup
import logging
from lxml import etree
import requests
import json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"

# Make sure that every link is formated so that there are no empty index at the front of the lists
getchu_urls = [
    "https://www.getchu.com/soft.phtml?id=1227327",
    "https://www.getchu.com/soft.phtml?id=1227328",
    "https://www.getchu.com/soft.phtml?id=1227329",
    "https://www.getchu.com/soft.phtml?id=1227330",
]

artists = [
           ['290786'],
           ['130658'],
           ['67731'],
           ['113780'],
           [''],
           [''],
           [''],
           
           ]

barcodes = ['4538806063067']


def is_kanji(char):
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  # CJK Unified Ideographs
        (cp >= 0x3400 and cp <= 0x4DBF) or  # CJK Unified Ideographs Extension A
        (cp >= 0x20000 and cp <= 0x2A6DF) or  # CJK Unified Ideographs Extension B
        (cp >= 0x2A700 and cp <= 0x2B73F) or  # CJK Unified Ideographs Extension C
        (cp >= 0x2B740 and cp <= 0x2B81F) or  # CJK Unified Ideographs Extension D
        (cp >= 0x2B820 and cp <= 0x2CEAF) or  # CJK Unified Ideographs Extension E
        (cp >= 0xF900 and cp <= 0xFAFF) or  # CJK Compatibility Ideographs
        (cp >= 0x2F800 and cp <= 0x2FA1F)):  # CJK Compatibility Ideographs Supplement
        return True
    else:
        return False

def create_getchu_session():
    """Create a requests session object to handle cookies automatically."""
    session = requests.Session()
    cookies = {'getchu_adalt_flag': 'getchu.com', }
    session.cookies.update(cookies)
    session.headers.update(HEADERS)
    return session


def parse_html(content):
    """
    Parse the HTML content using Beautiful Soup and return an lxml element.

    :param content: HTML content as bytes
    :return: lxml element
    """
    soup = BeautifulSoup(content, "html5lib")
    # print(soup.prettify())
    return etree.HTML(str(soup))


def extract_image_url(lxml_element, xpath):
    """
    Extract the image URL from the lxml element using the specified XPath.

    :param lxml_element: lxml element object
    :param xpath: XPath to locate the image element
    :return: Image URL as a string
    """
    image = lxml_element.xpath(xpath)
    if image:
        return image[0].get('href')
    else:
        raise ValueError('No image found at the specified XPath.')


def fetch_images(url):
    """
    Fetch the image URLs from a list of web addresses using the specified XPath.

    :param session: requests.Session() object
    :param web_addresses: List of URLs to fetch images from
    :param xpath: XPath to locate the image elements
    :return: List of image URLs
    """
    try:
        xpath = '//*[@id="soft_table"]/tbody/tr[1]/td/a'
        session = create_getchu_session()
        # print(session.cookies)

        # Make a GET request to the web address
        html_content = session.get(url).content
        # Parse the HTML content using Beautiful Soup and return an lxml element to use xpath
        lxml_element = parse_html(html_content)
        # get the getchu address for info later on
        # Extract the image URL from the lxml element using the specified XPath
        image_url = extract_image_url(lxml_element, xpath)

        # Make a GET request to the image URL
        session.headers.update(
            {'Referer': 'https://www.getchu.com/brandnew/1224951/c1224951package.jpg'})
        response = session.get("https://www.getchu.com/" + image_url[1:])
        response.raise_for_status()

        # Save the image to file
        title = lxml_element.xpath(
            '//*[@id="soft-title"]')[0].text.strip().split(" ")
        print(title)
        # ============ Entry Number + + Artist Name + GOT ============
        entry_name = ''.join(title[2:]) + "GOT"

        with open(f"{IMAGES_PATH}{entry_name}.jpg", "wb") as f:
            # Write the content of the response to the file
            f.write(response.content)

        return entry_name
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None


def fetch_info(url):
    info = {'price': None,
            'release_year': None,
            'release_month': None,
            'release_day': None,
            'barcode': None,
            'classifications_id': None
            }
    try:

        print(url)
        session = create_getchu_session()
        # Make a GET request to the web address
        html_content = session.get(url).content

        # Parse the HTML content using Beautiful Soup and return an lxml element to use xpath
        lxml_element = parse_html(html_content)

        # ======= extract the price and set it to the info dict =======
        price = lxml_element.xpath(
            '/html/body/div[1]/table[2]/tbody/tr[2]/th/table/tbody/tr[2]/td[2]')[0].text.strip().split(" ")
        info['price'] = int(price[0][1:6].replace(",", ""))
        print(f'success! price: {info["price"]}')
        
        # =================== Release Date ===================
        full_date = lxml_element.xpath('//*[@id="soft_table"]/tbody/tr[2]/th/table/tbody/tr[3]/td[2]/a')[0].text.strip().split("/")
        info['release_year'] = full_date[0]
        info['release_month'] = full_date[1]
        
        #Day is usually the only one that has kanji in it
        if(is_kanji(full_date[2][0]) == False):
            info['release_day'] = full_date[2]
        print(f'success! release date: {info["release_year"]}-{info["release_month"]}-{info["release_day"]}')
        
        # =================== Barcode ===================
        barcode = lxml_element.xpath('//*[@id="soft_table"]/tbody/tr[2]/th/table/tbody/tr[4]/td[2]')[0].text.strip()
        info['barcode'] = barcode
        print(f'success! barcode: {info["barcode"]}')
        
        # =================== Classification ID ===================
        title = lxml_element.xpath(
            '//*[@id="soft-title"]')[0].text.strip().split(" ")
        info["classifications_id"] = title[2]
        print(f'success! classification id: {info["classifications_id"]}')
        
        return info
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None


def create_entry_object(img_name: str, artists: str, classid: str, barcode: str, price: int, release_year: str, release_month: str, release_day: str, link: str):
    """
    Create a dictionary containing the image URLs and the entry name.

    Parameters
        index (int): Index of the image URL in the list
        companies: List of image URLs
        artists: list of artists
    """
    try:
        entry = {
            "root": "goods",
            "category": "on walls",
            "content_level": "nsfw",
            "image_name": f"{img_name}.jpg",
            "origins": ["9493"],  # ORIGINAL CHARACTERS
            "characters": [],
            "companies": ["62891"],  # GOT
            "artists": artists,
            # TAPESTRY, GOT TAPESTRY COLLECTION
            "classifications": ["23392", "108691"],
            "classifications_id" : classid, 
            "materials": ["41500"],  # DOUBLE SUEDE FABRIC
            "events": [],
            "release_year": release_year,
            "release_month": release_month,
            "release_day": release_day,
            "run": "standard",
            "notaxprice": price,
            "barcode": barcode,
            "size": "B2",
            "additional_info": "",
            "title": "",
            "original_title": "",
            "version": "",
            "original_ver": "",
            "width": None,
            "length": None,
            "height": None,
            "weight": None,
            "counterfeit": None,
            "links": [link]
        }

        # Load the existing JSON data from the file
        with open('data.json', 'r') as f:
            data = json.load(f)

        # Append a new object to the data
        data.clear()
        data.append(entry)

        # Write the updated data back to the file
        with open('data.json', 'w') as f:
            json.dump(data, f)

    except IndexError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


def main(index=0):

    if(getchu_urls[index] != ""):

        img_name = fetch_images(getchu_urls[index])
        print(f'Image URL: {img_name}')
        entry_info = fetch_info(getchu_urls[index])
        print(f'Entry Info: {entry_info}')

        index = getchu_urls.index(getchu_urls[index])
        create_entry_object(
        img_name, artists[index], entry_info['classifications_id'], entry_info['barcode'], entry_info['price'], entry_info['release_year'], entry_info['release_month'], entry_info['release_day'], getchu_urls[index]
                            )
        
        print('success! entry created')
        
if __name__ == "__main__":
    main()
