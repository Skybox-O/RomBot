from bs4 import BeautifulSoup
import requests

def temp(location):
    try:
        value = {'q': f"{location} weather"}  # the search terms
        response = requests.get("https://www.google.com/search?", params=value)
        if not response.ok:
            print(f"{response.status_code} {response.reason}")
    except Exception as e:
        print(f"{e}")

    html = BeautifulSoup(response.text, 'html.parser')

    weather = {}
    weather["Temperature"] = html.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    data = html.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text.split('\n')
    weather["Weather"] = data[1]
    weather["Time"] = data[0]

    if not weather:
        return None
    return weather