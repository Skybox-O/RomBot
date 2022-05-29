from Rom import visit
import sys


def scrape(url):
    games = {}
    html = visit(url)
    links = html.find_all('a')
    for a in links:
        link = a.get('href')
        if a.get_text() and check_num(link):
            games[a.get_text()] = link

    for key in games:
        print(f'{key} : {games[key]}')


def check_num(link):  # check if link is a rom link
    check = link.split('/')
    if len(check) >= 3:
        if check[2].isdigit():
            return True
    return False


if __name__ == "__main__":
    system = sys.argv[1]
    for i in range(65, 91):
        scrape(f'https://vimm.net/vault/{system}/{chr(i)}')