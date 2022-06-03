import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape(system):
    for i in range(65, 91):
        html = visit(f'https://vimm.net/vault/{system}/{chr(i)}')
        links = html.find_all('a')
        for a in links:
            link = a.get('href')
            if a.get_text() and check_num(link):
                title = a.get_text()
                html = visit(urljoin("https://vimm.net/vault/", link))
                media_id = html.find("input", attrs={'name': 'mediaId'}).get("value")
                print(f'{title} : {media_id}')


def visit(url):
    response = requests.get(url)
    if not response.ok:
        print(f"get_d_url({url}): {response.status_code} {response.reason}")
        raise Exception("Unable to Connect")
    return BeautifulSoup(response.text, 'html.parser')


def check_num(link):  # check if link is a rom link
    check = link.split('/')
    if len(check) >= 3:
        if check[2].isdigit():
            return True
    return False

if __name__ == "__main__":
    system = sys.argv[1]
    scrape(system)
