import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np


class DataFiller:
    url = 'https://www.tripadvisor.com'
    load_file = 'data.csv'
    save_file = 'data_loaded.csv'
    data = []
    loaded_data = []

    def __init__(self, url=None, load_file=None, save_file=None):
        if url:
            self.url = url
        if load_file:
            self.load_file = load_file
        if save_file:
            self.save_file = save_file
        self.data = pd.read_csv(self.load_file)

    def load_page(self, uri):
        r = requests.get(self.url+uri, allow_redirects=False)
        return bs(r.content, 'html.parser')

    def get_meals(self, cnt):
        block = cnt.find('div', {'class': '_3UjHBXYa'})
        if block:
            for child in block.children:
                if child.select('._14zKtJkz')[0].text == 'Meals':
                    return child.select('._1XLfiSsv')[0].text

    def get_rating(self, cnt):
        ratings_dict = {'Food': np.nan, 'Service': np.nan, 'Value': np.nan, 'Atmosphere': np.nan}
        rating_name = cnt.findAll('div', {'class': 'jT_QMHn2'})
        for i in rating_name:
            rate_name = i.select('span._2vS3p6SS')[0].text
            rate_value = int(i.find('span', {'class': 'ui_bubble_rating'})['class'][1][-2:])/10
            ratings_dict[rate_name] = rate_value
        return ratings_dict

    def load_data(self):
        counter = 0
        loaded_data = pd.DataFrame(columns=['ID_TA', 'Food Rating', 'Service Rating', 'Value Rating',
                                            'Atmosphere Rating', 'Meals'])
        for row in self.data.iloc:
            print(row['URL_TA'])
            print(counter, row['ID_TA'])
            page = self.load_page(row['URL_TA'])
            ratings = list(self.get_rating(page).values())
            meals = self.get_meals(page)
            print([row['ID_TA']] + ratings + [meals])
            loaded_data.loc[counter] = [row['ID_TA']] + ratings + [meals]
            counter += 1
            if counter > 10:
                break
        self.loaded_data = loaded_data
        return loaded_data

    def save_loaded_data(self):
        self.loaded_data.to_csv(self.save_file)
