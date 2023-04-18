from bs4 import BeautifulSoup
from lxml import etree
import requests
import json

IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"

#Make sure that every is formated so that there are no empty index at the front of the lists
web_addresses = [
        "https://comic.gotbb.jp/gps/Tapestry556_soitaro",
        "",
        "",
        "",
        "",
    ]

artists = [['314280']]

barcodes = ['4538806063067']

def create_session():
    """Create a requests session object to handle cookies automatically."""
    session_key = "eyJpdiI6IkZIS1k1MGpPeDNMVUlhaStReFwvelRnPT0iLCJ2YWx1ZSI6ImUxeHJUc0lGK1I1WDlRN0p5ZzdsU2g1RnRmNVhWanJEcUJaTVBOMENkQm5LUjVvaW5IdE5FV2Z4NHpTREkyaGExVkxUbDIyWmhqdmV5SU9YUFZFdFFBPT0iLCJtYWMiOiI0NTJjNTUwNDBmYmNiY2VkNzMxYWEyY2NkZjczZTQzMTY1YmI0YzRlYTRkZmViYWE3MTI3OTUzNmY3ZmE1ZTljIn0%3D"
    session = requests.Session()
    cookies2 = {'laravel_session': session_key}
    session.cookies.update(cookies2)
    return session


def pass_age_verification(session, verification_url, payload=None, headers=None):
    """
    Pass the age verification by sending a POST request with the required payload and headers.

    :param session: requests.Session() object
    :param verification_url: URL for age verification
    :param payload: Dictionary containing age verification fields
    :param headers: Dictionary containing custom headers, such as User-Agent
    :return: requests.Response object
    """
    response = session.post(verification_url, headers=headers)
    return response

def get_webpage_content(session, url):
    """
    Send an HTTP GET request to the specified URL and return the HTML content.

    :param session: requests.Session() object
    :param url: URL of the webpage
    :return: HTML content as bytes
    """
    response = session.get(url)
    return response.content

def parse_html(content):
    """
    Parse the HTML content using Beautiful Soup and return an lxml element.

    :param content: HTML content as bytes
    :return: lxml element
    """
    soup = BeautifulSoup(content, "html.parser")
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
        return image[0].get('src')
    else:
        raise ValueError('No image found at the specified XPath.')

def fetch_images(session, address, xpath):
    """
    Fetch the image URLs from a list of web addresses using the specified XPath.

    :param session: requests.Session() object
    :param web_addresses: List of URLs to fetch images from
    :param xpath: XPath to locate the image elements
    :return: List of image URLs
    """
    img_address = ""

    try:
        html_content = get_webpage_content(session, address)
        lxml_element = parse_html(html_content)
        image_url = extract_image_url(lxml_element, xpath)
        img_address = image_url
        # Make a GET request to the image URL
        response = requests.get("https://comic.gotbb.jp"+image_url)
        entry_name = address.split("/")[-1]
        
        with open(f"{IMAGES_PATH}{entry_name}.jpg", "wb") as f:
                # Write the content of the response to the file
                f.write(response.content)
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return img_address

def create_entry_object(index:int, artists:list , barcode: str, price:int, release_year:str, release_month:str, release_day:str):
    """
    Create a dictionary containing the image URLs and the entry name.

    Parameters
        index (int): Index of the image URL in the list
        companies: List of image URLs
        artists: list of artists
    """
    try:
        entry_name = web_addresses[index].split("/")[-1]
        
        entry = {
        "root": "goods", 
        "category": "on walls",
        "content_level": "nsfw",
        "image_name": f"{entry_name}.jpg",
        "origins": ["9493"],
        "characters": [],
        "companies": ["62891"],
        "artists": artists,
        "classifications": ["23392", "108691"],
        "materials": ["41500"],
        "events": [],
        "release_year": "2023",
        "release_month": "7",
        "release_day": "",
        "run": "standard",
        "notaxprice": 3900,
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
        "links": [web_addresses[index]]
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



def main():
    
    for address in web_addresses:
        if(address != ""):
            session = create_session()
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
            }
            
            pass_age_verification(session, address, headers)
            print(session.cookies)

            
            xpath = '//*[@id="dtR"]/img'

            img_addresses = fetch_images(session, address, xpath)
            print(img_addresses)
            index = web_addresses.index(address)
            create_entry_object(index, artists[index], barcodes[index], 3900, "2023", "7", "")

if __name__ == "__main__":
    main()
