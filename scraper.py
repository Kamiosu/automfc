from bs4 import BeautifulSoup
from lxml import etree
import requests

IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"
web_addresses = [
        "https://comic.gotbb.jp/gps/Tapestry552_komorikei",
    ]

def create_session():
    """Create a requests session object to handle cookies automatically."""
    session = requests.Session()
    cookies2 = {'laravel_session': 'eyJpdiI6ImF1VEo5TXp2aWNSWWZ6N05aWHpJQlE9PSIsInZhbHVlIjoiVEd0ejNtdDhcL0VubzNLY2xTUkh2MUtiSFVEeWsrektERmRmcHc4eXNuaFBJV3F2RUNvcGdwc3lEMEx4YzNCVVhUekRRNFd6d3BJU25ESHE3dXU0cVlBPT0iLCJtYWMiOiJiOTNiNmM3NDJiNmYzMDkwOGE4M2FiYzUxZjlhNjczMGMxNTg4MDg4NjY0YjJlNTdkY2EyMDA3Y2E3OTRlODk5In0%3D'}
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
    print(soup.prettify())
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

        with open(f"{IMAGES_PATH}testing.jpg", "wb") as f:
                # Write the content of the response to the file
                f.write(response.content)
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return img_address

def main():
    
    for address in web_addresses:
        session = create_session()
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        
        pass_age_verification(session, address, headers)
        print(session.cookies)

        
        xpath = '//*[@id="dtR"]/img'

        img_addresses = fetch_images(session, address, xpath)
        print(img_addresses)

if __name__ == "__main__":
    main()
