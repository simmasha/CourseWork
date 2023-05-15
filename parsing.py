import requests
from bs4 import BeautifulSoup
from transliterate import translit
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
import json

URLS = dict(CINEMA=dict(CINEMA_ACTION='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=action',
                        CINEMA_DRAMA='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=drama',
                        CINEMA_COMEDY='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=comedy',
                        CINEMA_ROMANCE='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=romance',
                        CINEMA_ADVENTURE='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=adventure',
                        CINEMA_THRILLER='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=thriller',
                        CINEMA_HORROR='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=horror',
                        CINEMA_FICTION='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=fiction',
                        CINEMA_CARTOON='https://afisha.yandex.ru/nizhny-novgorod/selections/cinema-today?filter=cartoon', ),
            CONCERT=dict(
                CONCERT_CLASSICAL_MUSIC='https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot?filter=classical_music',
                CONCERT_POP='https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot?filter=pop',
                CONCERT_ROCK='https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot?filter=rock',
                CONCERT_HIPHOP_RAP='https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot?filter=hiphop',
                CONCERT_METHAL='https://afisha.yandex.ru/nizhny-novgorod/selections/concert-hot?filter=metal'),
            THEATRE=dict(THEATRE_COMEDY='https://afisha.yandex.ru/nizhny-novgorod/selections/highrated-plays?filter=comedy',
                         THEATRE_DRAMA='https://afisha.yandex.ru/nizhny-novgorod/selections/highrated-plays?filter=drama',
                         THEATRE_MONOPERFORMANCE='https://afisha.yandex.ru/nizhny-novgorod/selections/highrated-plays?filter=monoperformance',
                         THEATRE_MUSICAL='https://afisha.yandex.ru/nizhny-novgorod/musical?source=menu'),
            SHOW=dict(SHOW_STANDUP='https://afisha.yandex.ru/nizhny-novgorod/show?source=menu&filter=standup',
                      SHOW_KIDS='https://afisha.yandex.ru/nizhny-novgorod/show?source=menu&filter=kids',
                      SHOW_NON_CHILDREN='https://afisha.yandex.ru/nizhny-novgorod/show?source=menu&filter=non-children'))

HEADERS = {
    "Accept": '*/*',
    "User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36'
}


def Parsing():
    events = {'ID': [], 'category': [], 'subcategory': [], 'title': [], 'place': [], 'date': [], 'image': [],
              'link': []}
    for CATEGORY, SUBCATEGORIES in URLS.items():
        for SUBCATEGORY in SUBCATEGORIES:
            REQUEST = requests.get(URLS.get(CATEGORY).get(SUBCATEGORY), headers=HEADERS)
            SRC = REQUEST.text
            SOUP = BeautifulSoup(SRC, 'lxml')

            TITLES = SOUP.find_all(attrs={"data-component": "EventCard__EventInfo__Title"})
            DETAILS = SOUP.find_all(attrs={"data-component": "EventCard__EventInfo__Details"})
            LINKS = SOUP.find_all(attrs={"data-testid": "event-card-link"})
            IMAGES = SOUP.find_all(attrs={"data-component": "EventCard__Cover"})

            for i in range(len(LINKS)):
                category = str(CATEGORY)
                subcategory = str(SUBCATEGORY)
                title = TITLES[i].text
                time = DETAILS[i].find('li').text
                place = DETAILS[i].find('li').find_next_sibling()
                ID = idGeneration(title, time)


                events['ID'].append(ID)
                events['category'].append(category)
                events['subcategory'].append(subcategory)
                events['title'].append(title)
                events['date'].append(time)
                if place:
                    events['place'].append(DETAILS[i].find('li').find_next_sibling().text)
                else:
                    events['place'].append("None")
                events['link'].append(f'https://afisha.yandex.ru{LINKS[i].get("href")}')
                img = IMAGES[i].find('img')
                if img:
                    events['image'].append(img.get('src'))
                else:
                    events['image'].append("None")

            with open(f"events/{CATEGORY}.json", "w") as file:
                json.dump(events, file, indent=4, ensure_ascii=False)

            data = pd.DataFrame(events)
            table = pa.Table.from_pandas(data)
            with pq.ParquetWriter('eventsDB.parquet', table.schema) as writer:
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
