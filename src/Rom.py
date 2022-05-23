import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch(rom_info):  # fetches rom from vimm.net
    try:
        url = f'https://vimm.net/?p=vault'
        rom_info = rom_info.split(' : ')
        relative = create_path(rom_info[0], rom_info[1])
        absolute = urljoin(url, relative)
        download(absolute)
    except Exception as E:
        print(E)


def download(url):
    payload = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "download2.vimm.net",
        "Referer": "https://vimm.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    html = visit(url)
    media_id = html.find("input", attrs={'name': 'mediaId'}).get("value")
    url_d = f'https://download2.vimm.net/download/?mediaId={media_id}'

    response = requests.get(url_d, headers=payload)
    print(response.headers.get("filename"))
    open('filename.zip', 'wb').write(response.content)
    if not response.ok:
        print(f"get_rom({url}): {response.status_code} {response.reason} {response.headers}")
        raise Exception("Unable to Connect")


def visit(url):  # tries to visit a webpage returns the html
    response = requests.get(url)
    if not response.ok:
        print(f"get_rom({url}): {response.status_code} {response.reason}")
        raise Exception("Unable to Connect")
    html = BeautifulSoup(response.text, 'html.parser')
    return html


def create_path(system, title): # locates and returns relative path from rom titles in respective system
    if system not in ["SNES", "NES", "GameCube", "PS1", 'PS3']:
        raise Exception(f"Invalid System")

    with open(f'../data/{system}_data') as f:
        for line in f:
            if title in line:
                relative = line.strip('\n').split(' /')[1]
                return relative

        raise Exception(f"Invalid Rom")


fetch("SNES : Street Fighter II")
