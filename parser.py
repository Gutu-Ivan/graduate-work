import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

# Getting apartments
aps, ap_links, names, prices, price_per_square_list, area, rooms, floors = [], [], [], [], [], [], [], []
for i in range(1, 10):
    URL = "https://999.md/ru/list/real-estate/apartments-and-rooms?hide_duplicates=no&sort_type=price_asc&applied=1&show_all_checked_childrens=yes&sort_expanded=yes&ef=32,31,33,2203,30,1073,1191&eo=12900,13859,12912,12885&o_32_8_12900=13859&r_31_2_from=&r_31_2_to=1000000&r_31_2_unit=eur&o_33_1=776&o_2203_795=18895,18894,20364&o_30_241=893,894,902,904,20442&r_1073_244_from=1&r_1073_244_to=2000&r_1073_244_unit=m2&o_1191_248=918,935,905,929,909,955,895,921,934,947,970,965&aof=1191&page=" + str(i)
    page = requests.get(URL)

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('div', 'ads-list-photo-item-title')
    for job in jobs:
        aps.append(job.get_text())
        children = job.findChildren("a", recursive=False)
        for child in children:
            ap_links.append('https://999.md' + child['href'])

    for job_link in ap_links:
        response = requests.get(job_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = getattr(soup.find("header", class_="adPage__header"), 'text', None)
        price = soup.find("span", class_="adPage__content__price-feature__prices__price__value")
        price_per_square = getattr(soup.find("span", class_="adPage__content__price-feature__labels__price-per-m__value"), 'text', None)

        names.append(name)
        prices.append(price.string)
        price_per_square_list.append(price_per_square)

        # Characteristics
        characteristics = soup.find("div", class_="adPage__content__features__col grid_9 suffix_1").find_all("ul")

        for ul in characteristics:
            for li in ul:
                el = getattr(li.find('span'), 'text', None)
                if el == ' Общая площадь ':
                    value = li.find("span", class_="adPage__content__features__value")
                    area.append(value.string)
                elif el == ' Количество комнат ':
                    value = li.find("span", class_="adPage__content__features__value")
                    rooms.append(value.string)
                elif el == ' Этаж ':
                    value = li.find("span", class_="adPage__content__features__value")
                    floors.append(value.string)
    print('Page nr.' + str(i) + ' was parsed')

# Saving to csv file
filepath = Path('apartments.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame({'Name': names,
                   'Price': prices,
                   'Price per square': price_per_square_list,
                   'Area': area,
                   'Rooms': rooms,
                   'Floor': floors
                   })
df.to_csv(filepath)
print('Done!')
