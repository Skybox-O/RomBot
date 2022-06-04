import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from os.path import exists


def fetch(rom_request):  # fetches rom from vimm.net | request format = "system : title"
    url = 'https://vimm.net/?p=vault'
    sys_rom = rom_request.split(': ')
    rom_data = parse_data(sys_rom[0], sys_rom[1])  # rom_data == {file_name: NAME, media_id: ID}

    if not exists(f'/home/skyler/RomLib/{rom_data["file_name"]}.zip'):  # if the rom is not in the library download the rom
        download_rom(rom_data)
    return (f'/home/skyler/RomLib/{rom_data["file_name"]}.zip')


def parse_data(system, title):  # locates and returns rom data from the systems data file
    if not exists(f'/home/skyler/RomBot/data/{system}_data'):
        raise Exception("Invalid System")

    with open(f'/home/skyler/RomBot/data/{system}_data') as data_file:
        for line in data_file:
            if title in line:
                data = line.strip('\n').split(' : ')
                rom_data = {"file_name": data[0].replace(" ", "-"), "media_id": data[1]}
                return rom_data
        # if title doesn't match any rom's title in data file
        raise Exception("Invalid Rom")


def download_rom(rom_data):
    payload = {  # payload to make request look like a user
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "download2.vimm.net",
        "Referer": "https://vimm.net/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }

    # create the download link
    d_url = f'https://download2.vimm.net/download/?mediaId={rom_data["media_id"]}'

    # download the .zip file and save it into the Rom Library
    response = requests.get(d_url, headers=payload)
    if not response.ok:
        print(f"download({d_url}): {response.status_code} {response.reason} {response.headers}")
        raise Exception("Unable to Download")

    open(f'/home/skyler/RomLib/{rom_data["file_name"]}.zip', 'wb').write(response.content)
    print("Finished Download.")



if __name__ == "__main__":
    try:
        print(fetch(' '.join(sys.argv[1:])))
    except Exception as E:
        print(E)
