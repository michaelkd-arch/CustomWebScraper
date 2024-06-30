from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

URL = 'https://www.nike.com/bg/w/mens-shoes-nik1zy7ok'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/126.0.0.0 Safari/537.36'
}

element = 'div'
element_class = 'product-card__info'
nested_e = 'div'
nested_e_class = 'product-card__title'
nested_e2 = 'div'
nested_e2_class = 'product-price'
csv_path = 'Nike_Sneakers/nike_sneakers.csv'


class CustomWebScraper:
    def __init__(self):
        self.url = URL
        self.headers = HEADERS
        self.element = element
        self.element_class = element_class
        self.nested_e = nested_e
        self.nested_e_class = nested_e_class
        self.nested_e2 = nested_e2
        self.nested_e2_class = nested_e2_class
        self.models = []
        self.prices = []
        self.csv_path = csv_path

    def scrape(self):
        response = requests.get(url=self.url, headers=self.headers)
        print(response.status_code)
        contents = response.text
        soup = BeautifulSoup(contents, 'lxml')
        elements = soup.find_all(self.element, attrs={'class': self.element_class})
        for e in elements:
            model = e.find_next(self.nested_e, attrs={'class': self.nested_e_class})
            price = e.find_next(self.nested_e2, attrs={'class': self.nested_e2_class})
            self.models.append(model.text)
            self.prices.append(price.text.replace('\xa0', ' '))
            df = pd.DataFrame({'Product Name': self.models, 'Price': self.prices})
            df.to_csv(self.csv_path, index=False, encoding='utf-8')
        print('Ready')


cws = CustomWebScraper()
cws.scrape()
