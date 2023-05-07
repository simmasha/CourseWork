import requests
from bs4 import BeautifulSoup
import json
from transliterate import translit
import pandas as pd

URLS = dict(CINEMA="https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today",
            CONCERT="https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot",
            THEATRE="https://afisha.yandex.ru/nizhny-novgorod/selections/highrated-plays",
            PUSHKIN_CARD="https://afisha.yandex.ru/nizhny-novgorod/pushkin-card?source=menu",
            QUEST="https://afisha.yandex.ru/nizhny-novgorod/quest?source=menu",
            SHOW="https://afisha.yandex.ru/nizhny-novgorod/show?source=menu",
            STANDUP="https://afisha.yandex.ru/nizhny-novgorod/standup?source=menu",
            EXCURSION="https://afisha.yandex.ru/nizhny-novgorod/excursions?source=menu",
            MUSICAL="https://afisha.yandex.ru/nizhny-novgorod/musical?source=menu",
            MASTERCLASS="https://afisha.yandex.ru/nizhny-novgorod/masterclass?source=menu",
            )

headers = {
    "Accept": '*/*',
    "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
}

def Parsing():
    df = None
    for URL in URLS:
        req = requests.get(URLS.get(URL), headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        events = {}
        titles = soup.find_all(attrs={"data-component": "EventCard__EventInfo__Title"})
        details = soup.find_all(attrs={"data-component": "EventCard__EventInfo__Details"})
        hrefs = soup.find_all(attrs={"data-testid": "event-card-link"})
        imgs = soup.find_all(attrs={"data-component": "EventCard__Cover"})
        for i in range(len(hrefs)):
            title = titles[i].text

            events[title] = []
            events[title].append(details[i].find('li').text)
            if details[i].find('li').find_next_sibling(): events[title].append(details[i].find('li').find_next_sibling().text)
            else: events[title].append(None)
            events[title].append('https://afisha.yandex.ru' + hrefs[i].get("href"))
            img = imgs[i].find('img')
            if img:
                img_href = img.get('src')
                events[title].append(img_href)
            else: events[title].append(None)

        with open(f"events/{URL}.json", "w") as file:
            json.dump(events, file, indent=4, ensure_ascii=False)

    return events

def idGeneration(name: str, date: str, city = "NN") -> str:
    return "-".join("-".join(date.split("."), ) + city + translit(name, language_code="ru", reversed=True))