from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep
import random
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
]

profile = FirefoxProfile()

random_user_agent = random.choice(user_agents)
profile.set_preference("general.useragent.override", random_user_agent)

firefox_options = Options()
firefox_options.profile = profile

driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
driver.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
sleep(10)
driver.implicitly_wait(20)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
elems = driver.find_elements(by=By.XPATH,value="//a[@href]")
allLink = []
for elem in elems:
    links = elem.get_attribute("href")
    allLink.append(links)

filmLinks = []
for link in allLink:
    pattern = re.compile(r"https://www\.imdb\.com/title/", re.IGNORECASE)
    if pattern.match(link):
        filmLinks.append(link)

clean_urls = [re.match(r"(https://www\.imdb\.com/title/tt\d+)/", url).group(1) + "/" for url in filmLinks]
filmLinks = list(set(clean_urls))


driver.close()

print(len(filmLinks))
dataset = []

for link in filmLinks:
    print(link)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find("span", class_='hero__primary-text')
    title = title_tag.get_text(strip=True) if title_tag else ""

    ulsCast = soup.find_all("ul", class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')
    directors = [a.get_text(strip=True) for a in ulsCast[0].find_all("a")] if len(ulsCast) > 0 else []
    writers   = [a.get_text(strip=True) for a in ulsCast[1].find_all("a")] if len(ulsCast) > 1 else []
    stars     = [a.get_text(strip=True) for a in ulsCast[2].find_all("a")] if len(ulsCast) > 2 else []

    uls = soup.find("ul", class_='ipc-inline-list ipc-inline-list--show-dividers sc-cb6a22b2-2 aFhKV baseAlt baseAlt')
    if uls:
        items = [li.get_text(strip=True) for li in uls.find_all("li")]
        year = items[0] if len(items) > 0 else ""
        rating = items[1] if len(items) > 1 else ""
        duration = items[2] if len(items) > 2 else ""
    else:
        year, rating, duration = "", "", ""

    genre_div = soup.find('div', class_='ipc-chip-list__scroller')
    genre = [span.get_text(strip=True) for span in genre_div.find_all("span")] if genre_div else []

    gross = soup.find("li", {"data-testid": "title-boxoffice-grossdomestic"})
    gross_us_canada = gross.find("span", class_="ipc-metadata-list-item__list-content-item").get_text(strip=True) if gross else ""

    path = urlparse(link).path
    parts = path.strip("/").split("/")
    fullId = parts[1] if len(parts) > 1 else ""
    id = fullId.lstrip("tt") if fullId else ""

    data = {
        "id": id if id else None,
        "title": title if title else None,
        "directors": ", ".join(directors) if directors else None,
        "writers": ", ".join(writers) if writers else None,
        "stars": ", ".join(stars) if stars else None,
        "year": year if year else None,
        "rating": rating if rating else None,
        "duration": duration if duration else None,
        "genre": ", ".join(genre) if genre else None,
        "gross_us_canada": gross_us_canada if gross_us_canada else None
    }

    dataset.append(data)

print(dataset)

df = pd.DataFrame(dataset)
df.to_csv("imdb_top_movies.csv", index=False, encoding="utf-8-sig")
