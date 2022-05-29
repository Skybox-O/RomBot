import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from os.path import exists
import json

# with open("/home/skyler/RomBot/src/config.json") as json_conf:
#     CONF = json.load(json_conf)

def fetch(rom_request):  # fetches rom from vimm.net | request format = "system : title"
    try:
        url = f'https://vimm.net/?p=vault'
        rom_request = rom_request.split(' : ')
        rom_data = parse_data(rom_request[0], rom_request[1]) # rom_data == [title, relative_path]
        absolute = urljoin(url, rom_data[1])
        file_name = rom_data[0].replace(" ", "-")

        if not exists(f'/home/skyler/RomLib/{file_name}.zip'): # if the rom is not in the library download the rom
            download(absolute, file_name)
        print(f'/home/skyler/RomLib/{file_name}.zip')

    except Exception as E:
        print(E)


def parse_data(system, title): # locates and returns rom data from the systems data file
    if not exists(f'/home/skyler/RomBot/data/{system}_data'):
        raise Exception(f"Invalid System")

    with open(f'/home/skyler/RomBot/data/{system}_data') as data_file:
        for line in data_file:
            if title in line:
                data = line.strip('\n').split(' : ')
                return data
        # if title doesn't match any rom's in data file
        raise Exception(f"Invalid Rom")


def download(url, file_name):
    payload = {  # payload to make request look like a user
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

    # get the correct mediaId for the download link
    media_id = html.find("input", attrs={'name': 'mediaId'}).get("value")
    d_url = f'https://download2.vimm.net/download/?mediaId={media_id}'

    # download the .zip file and save it into the Rom Library
    response = requests.get(d_url, headers=payload)
    if not response.ok:
        print(f"get_rom({url}): {response.status_code} {response.reason} {response.headers}")
        raise Exception("Unable to Download")

    open(f'/home/skyler/RomLib/{file_name}.zip', 'wb').write(response.content)
    print("Finished Download.")


if __name__ == "__main__":
    fetch(' '.join(sys.argv[1:]))
