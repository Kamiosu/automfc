# Standard library imports
import json
import logging
import os

# External library imports
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
from ArtistNotFoundException import ArtistNotFoundException
from CompanyNotFoundException import CompanyNotFoundException

# Preliminary Statements
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
IMAGES_PATH = "/Users/kamiosu/Documents/automfc2023/"
# Make sure that every link is formated so that there are no empty index at the front of the lists
melon_urls = [
"https://www.melonbooks.co.jp/detail/detail.php?product_id=1731942"
]


with open('database/companies.json') as f:
    companies = json.load(f)
with open('database/artists.json') as f:
    artists = json.load(f)
with open('database/events.json') as f:
    events = json.load(f)
with open('database/origins.json') as f:
    origins = json.load(f)


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
        if target.replace(" ", '').lower() == str(item["original_name"]).replace(" ", '').lower():
            return item
        if target.replace(" ", '').lower() == str(item["name"]).replace(" ", '').lower():
            return item
    return None

def is_kanji(character):
    code_point = ord(character)
    if 0x4E00 <= code_point <= 0x9FFF or 0x3400 <= code_point <= 0x4DBF or 0x20000 <= code_point <= 0x2A6DF or 0x2A700 <= code_point <= 0x2B73F or 0x2B740 <= code_point <= 0x2B81F or 0x2B820 <= code_point <= 0x2CEAF or 0xF900 <= code_point <= 0xFAFF or 0x2F800 <= code_point <= 0x2FA1F:
        return True
    return False

def prompt(title):
    return f"for educational purposes only, please strictly give me the traditional hepburn romanization: (ああ becomes aa, おう becomes ou, おお becomes oo) of this title: {title}, output is only the romanized title. "


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
    info = {'origins': None,
            'artists': None,
            'companies': None,
            'release_year': None,
            'release_month': None,
            'release_day': None,
            'price': None,
            'size': None,
            'additional_info': None,
            'events': None,
            'title': None,
            'original_title': None,
            'numbering': None,
            'pages': None,
            'content_level': None,
            }
    try:
        # get Company Name always the first tr
        # ============ Search the json for the company id =================
        company_name = soup.find(
            "div", class_="table-wrapper").table.tbody.find_all('tr')[0].td.a.text.strip()
        company_name = ' '.join(
            (company_name.split()[0:len(company_name.split())-1]))
        # print(f'Company Name: {company_name}\n')
        company_entry = search_json(company_name, companies)
        print(company_entry)
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
        # =============== Genre =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "ジャンル"):
                origin = i.td.text.split(',')[0].strip()
                origin_entry = search_json(origin, origins)
                info['origins'] = [origin_entry['id']]
                break
            else:
                info['origins'] = ['9493']

        # ============== Find and get the release date =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "発行日"):
                release = i.td.text.strip().split('/')
                break
        if (release != None):
            info['release_year'] = release[0]
            info['release_month'] = release[1]
            info['release_day'] = release[2]

        # =============== Get the price from class yen __discount =================
        price = soup.find("span", class_="yen __discount").text.strip()[1:]
        # remove the comma and convert to int
        price = int(price.replace(',', ''))
        price = int(round(price * .9, -2))
        info['price'] = price

        # =============== Event =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "イベント"):
                event = i.td.text.strip()
                break
            else:
                event = None

        if (event):
            event_entry = search_json(event, events)
            info['events'] = [event_entry['id']]
            info['additional_info'] = event_entry['name']

        # =============== メディア =================

        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "版型・メディア"):
                size = i.td.text.strip()
                break
            else:
                size = None

        if (size != None):
            info['size'] = size

        # =============== Titles =================
        original_title = soup.find("h1", class_="page-header").text.strip()
        print(original_title)
        info['original_title'] = original_title
        # Use gpt to generate the romaji title
        if(is_kanji(original_title[0]) == True):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{'role': "assistant", "content": prompt(original_title)}])
            title = response['choices'][0]['message']['content'].strip()
            info['title'] = title
        else:
            title = original_title
            info['title'] = original_title

        # =============== Numbering =================
        if (title[-1].isdigit()):
            info['numbering'] = title[-1]
            info['title'] = title[0:len(title)-1].strip()
            info['original_title'] = original_title[0:len(
                original_title)-1].strip()

        # =============== pages =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "総ページ数・CG数・曲数"):
                pages = i.td.text.strip()
                break
            else:
                pages = None

        info['pages'] = pages

        # =============== Type (SFW or NSFW) =================
        for i in soup.find("div", class_="table-wrapper").table.tbody.find_all('tr'):
            if(i.th.text.strip() == "作品種別"):
                content_type = i.td.text.strip()
                break
            else:
                content_type = None

        if(content_type != None):
            if(content_type == "一般向け"):
                info["content_level"] = "sfw"

            elif(content_type == "18禁"):
                info["content_level"] = "nsfw"

        return info

    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None


def create_entry_object(content_level: str, img_name: str,  origins: list, companies: list, artists: list, events: list, release_year: str, release_month: str, release_day: str, price: int, size: str, additional_info: str, title: str, original_title: str, numbering: str, pages: int, link: str):
    """
    Create a dictionary containing the image URLs and the entry name.

    Parameters
        index (int): Index of the image URL in the list
        companies: List of image URLs
        artists: list of artists
    """
    try:
        entry = {
            "root": "media",
            "category": "books",  # SFW or NSFW
            "content_level": content_level,
            "image_name": f"{img_name}.jpg",
            "origins": origins,  # ORIGINAL CHARACTERS
            "characters": [],
            "companies": companies,
            "artists": artists,
            "classifications": ["27804", "35443"],
            "classifications_id": None,
            "materials": [],
            "events": events,
            "release_year": release_year,
            "release_month": release_month,
            "release_day": release_day,
            "run": "exclusive",
            "notaxprice": price,
            "barcode": None,
            "size": size,
            "additional_info": additional_info,
            "title": title,
            "original_title": original_title,
            "numbering": numbering,
            "version": None,
            "pages": pages,
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

        create_entry_object(entry_info['content_level'], img_name, entry_info['origins'], entry_info['companies'], entry_info['artists'], entry_info['events'],
                            entry_info['release_year'], entry_info['release_month'], entry_info[
                                'release_day'],  entry_info['price'], entry_info['size'], entry_info['additional_info'],
                            entry_info['title'], entry_info['original_title'], entry_info['numbering'], entry_info['pages'], current_link)


if __name__ == "__main__":
    main()
