from bs4 import BeautifulSoup
import logging
import requests
import json
from ArtistNotFoundException import ArtistNotFoundException
from CompanyNotFoundException import CompanyNotFoundException
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"

# Make sure that every link is formated so that there are no empty index at the front of the lists
melon_urls = [
 
]

with open('database/companies.json') as f:
    companies = json.load(f)
with open('database/artists.json') as f:
    artists = json.load(f)


def create_melon_session():
    """Create a requests session object to handle cookies automatically."""
    session = requests.Session()
    cookies = {'AUTH_ADULT': '1'}
    session.cookies.update(cookies)
    session.headers.update(HEADERS)
    session.headers.update({'Referer': 'https://www.melonbooks.co.jp/circle/index.php?circle_id=16213&orderby=publish_start_date&disp_number=100&pageno=1&is_sp_view=&fromagee_flg=2&search_target_all=0&additional_all=1&product_type=0&is_end_of_sale%5B%5D=1&is_end_of_sale2=1&text_type=all&name='})
    return session


def search_json(target, data):
    for item in data:
        if target.replace(" ", '').lower() == str(item["original_name"]).replace(" ",'').lower():
            return item
        if target.replace("", '').lower() == str(item["name"]).replace(" ",'').lower():
            return item
    return None


def parse_html(request):
    """
    Parse the HTML content using Beautiful Soup and return an lxml element.

    :param content: HTML content as bytes
    :return: lxml element
    """
    soup = BeautifulSoup(request, "html5lib")
    open('melon.html', 'w').write(soup.prettify())

    return soup


def fetch_images(url, session, soup):
    """
    Fetch the image URLs from a list of web addresses using the specified XPath.

    :param session: requests.Session() object
    :param web_addresses: List of URLs to fetch images from
    :param xpath: XPath to locate the image elements
    :return: List of image URLs
    """
    try:
        # Get the image URL from the soup element
        image_url = soup.find('div', class_='slider').a.get('href')

        # Make a GET request to the image URL
        response = session.get("https://"+image_url[2:], verify=True)
        response.raise_for_status()

        # Save the image to file
        artist_name = soup.find(
            "div", class_="table-wrapper").table.tbody.find_all('tr')[1].td.a.text.strip()
        title = url.strip().split('=')[-1] + artist_name
        # print(title)
        # ============ Entry Number + + Artist Name + GOT ============
        entry_name = ''.join(title) + "Melon"

        with open(f"{IMAGES_PATH}{entry_name}.jpg", "wb") as f:
            # Write the content of the response to the file
            f.write(response.content)

        return entry_name
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None


def fetch_info(soup):
    info = {'price': None,
            'artists': None,
            'companies': None,
            'release_year': None,
            'release_month': None,
            'release_day': None,
            'content_level': None,
            }
    try:
        # get Company Name always the first tr
        # ============ Search the json for the company id =================
        company_name = soup.find(
            "div", class_="table-wrapper").table.tbody.find_all('tr')[0].td.a.text.strip()
        company_name = company_name.split()[0]
        print(f'Company Name: {company_name}\n')
        company_entry = search_json(company_name, companies)

        if(company_entry != None):
            info['companies'] = [company_entry['id']]
        else:
            raise CompanyNotFoundException(company_name)

        # ============   Get artist name always the second tr =================
        artist_name = soup.find(
            "div", class_="table-wrapper").table.tbody.find_all('tr')[1].td.a.text.strip()
        artist_entry = search_json(artist_name, artists)

        if(artist_entry != None):
            info['artists'] = [artist_entry['id']]
        else:
            raise ArtistNotFoundException(artist_name)

        # ============== Find and get the release date =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "発行日"):
                release = i.td.text.strip().split('/')
                break
        info['release_year'] = release[0]
        info['release_month'] = release[1]
        info['release_day'] = release[2]

        # =============== Get the price from class yen __discount =================
        price = soup.find("span", class_="yen __discount").text.strip()[1:]
        # remove the comma and convert to int
        price = int(price.replace(',', ''))
        price = int(round(price * .9, -2))
        info['price'] = price

        # =============== Type (SFW or NSFW) =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "作品種別"):
                type = i.td.text.strip()
                break

        if(type == "一般向け"):
            info["content_level"] = "sfw"

        elif(type == "18禁"):
            info["content_level"] = "nsfw"

        return info

    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None


def create_entry_object(img_name: str, artists: list, companies: list, price: int, release_year: str, release_month: str, release_day: str, content_level: str, link: str):
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
            "category": "on walls",  # SFW or NSFW
            "content_level": content_level,
            "image_name": f"{img_name}.jpg",
            "origins": ["9493"],  # ORIGINAL CHARACTERS
            "characters": [],
            "companies": companies,
            "artists": artists,
            "classifications": ["23392"],
            "classifications_id": None,
            "materials": ["41500"],  # DOUBLE SUEDE FABRIC
            "events": [],
            "release_year": release_year,
            "release_month": release_month,
            "release_day": release_day,
            "run": "standard",
            "notaxprice": price,
            "barcode": None,
            "size": "B2",
            "additional_info": None,
            "title": None,
            "original_title": None,
            "version": None,
            "original_ver": None,
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
            json.dump(data, f, ensure_ascii=False)

    except IndexError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


def main(index=0):

    if(melon_urls[index] != ""):
        session = create_melon_session()
        # print(session.cookies)

        # Make a GET request to the web address
        current_link = melon_urls[index].replace(" ", "")
        request = session.get(
            current_link+"&adult_view=1", verify=True).content
        # Parse the HTML content using Beautiful Soup
        soup = parse_html(request)
        img_name = fetch_images(current_link, session, soup)
        print(f'Image File Name: {img_name}.jpg\n')
        entry_info = fetch_info(soup)
        print(f'Entry Info: {entry_info}\n')

        create_entry_object(img_name, entry_info['artists'], entry_info['companies'], entry_info['price'], entry_info['release_year'],
                            entry_info['release_month'], entry_info['release_day'], entry_info['content_level'], current_link)


if __name__ == "__main__":
    main()
