import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from os.path import exists


def fetch(rom_info):  # fetches rom from vimm.net
    try:
        url = f'https://vimm.net/?p=vault'
        rom_info = rom_info.split(' : ')
        rom_data = parse_data(rom_info[0], rom_info[1]) # rom_data == [title, relative_path]
        absolute = urljoin(url, rom_data[1])
        save_path = ''
        if exists(f'/home/skyler/RomLib/{rom_data[0]}.zip'):
            print(f'/home/skyler/RomLib/{rom_data[0]}.zip')
        else:
            download(absolute, rom_data[0])
    except Exception as E:
        print(E)


def parse_data(system, title): # locates and returns rom data from the systems data file
    if system not in ["SNES", "NES", "GameCube", "PS1", 'PS3']:
        raise Exception(f"Invalid System")

    with open(f'/home/skyler/RomBot/data/{system}_data') as f:
        for line in f:
            if title in line:
                data = line.strip('\n').split(' : ')
                return data

        raise Exception(f"Invalid Rom")


def download(url, file_name):  # downloads rom.zip from vimms liar
    payload = {  # pyaload to make request seem like a user not a bot
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "download2.vimm.net",
        "Referer": "https://vimm.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(url)
    if not response.ok:
        print(f"get_rom({url}): {response.status_code} {response.reason}")
        raise Exception("Unable to Connect")
    html = BeautifulSoup(response.text, 'html.parser')

    media_id = html.find("input", attrs={'name': 'mediaId'}).get("value")
    url_d = f'https://download2.vimm.net/download/?mediaId={media_id}'

    response = requests.get(url_d, headers=payload)
    save_path = '/home/skyler/RomLib'
    open(f'{save_path}/{file_name}.zip', 'wb').write(response.content)
    if not response.ok:
        print(f"get_rom({url}): {response.status_code} {response.reason} {response.headers}")
        raise Exception("Unable to Download")

if __name__ == "__main__":
    fetch(' '.join(sys.argv[1:]))
