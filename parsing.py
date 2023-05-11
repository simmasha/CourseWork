import requests
from bs4 import BeautifulSoup
from transliterate import translit
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
import json

URLS = dict(CINEMA="https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today",
            CONCERT="https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot",
            THEATRE="https://afisha.yandex.ru/nizhny-novgorod/selections/highrated-plays",
            PUSHKIN_CARD="https://afisha.yandex.ru/nizhny-novgorod/pushkin-card?source=menu",
            # QUEST="https://afisha.yandex.ru/nizhny-novgorod/quest?source=menu",
            SHOW="https://afisha.yandex.ru/nizhny-novgorod/show?source=menu",
            STANDUP="https://afisha.yandex.ru/nizhny-novgorod/standup?source=menu",
            EXCURSION="https://afisha.yandex.ru/nizhny-novgorod/excursions?source=menu",
            MUSICAL="https://afisha.yandex.ru/nizhny-novgorod/musical?source=menu",
            MASTERCLASS="https://afisha.yandex.ru/nizhny-novgorod/masterclass?source=menu",
            )

HEADERS = {
    "Accept": '*/*',
    "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
}


def Parsing():
    events = {'ID': [], 'category': [], 'titles': [], 'place': [], 'time': [], 'img': [], 'href': []}
    for URL in URLS:
        REQUEST = requests.get(URLS.get(URL), headers=HEADERS)
        SRC = REQUEST.text
        SOUP = BeautifulSoup(SRC, 'lxml')

        TITLES = SOUP.find_all(attrs={"data-component": "EventCard__EventInfo__Title"})
        DETAILS = SOUP.find_all(attrs={"data-component": "EventCard__EventInfo__Details"})
        LINKS = SOUP.find_all(attrs={"data-testid": "event-card-link"})
        IMAGES = SOUP.find_all(attrs={"data-component": "EventCard__Cover"})

        for i in range(len(LINKS)):
            category = str(URL)
            title = TITLES[i].text
            time = DETAILS[i].find('li').text
            place = DETAILS[i].find('li').find_next_sibling()
            ID = idGeneration(title, time)

            events['ID'].append(ID)
            events['category'].append(category)
            events['titles'].append(title)
            events['time'].append(time)
            if place:
                events['place'].append(DETAILS[i].find('li').find_next_sibling().text)
            else:
                events['place'].append("None")
            events['href'].append(f'https://afisha.yandex.ru{LINKS[i].get("href")}')
            img = IMAGES[i].find('img')
            if img:
                events['img'].append(img.get('src'))
            else:
                events['img'].append("None")

        with open(f"events/{URL}.json", "w") as file:
            json.dump(events, file, indent=4, ensure_ascii=False)

        data = pd.DataFrame(events)
        table = pa.Table.from_pandas(data)
        with pq.ParquetWriter('events_file.parquet', table.schema) as writer:
            writer.write_table(table)


def idGeneration(name: str, date: str, city="NN") -> str:
    name = translit(name, language_code='ru', reversed=True)
    date = translit(date, language_code='ru', reversed=True)
    name = name.split(" ")
    ID = city
    for word in name:
        ID += word[0]
    return ID
    # return "-".join("-".join(date.split("."), ) + city + translit(name, language_code="ru", reversed=True))
