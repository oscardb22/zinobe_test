from datetime import datetime
from littlenv import littlenv
import requests
import hashlib
import pandas as pd
import os
import sqlite3

littlenv.load()


class TestZinobe:
    url_countries = os.environ.get('url_countries', None)
    url_country = os.environ.get('url_country', None)
    url_name_country = os.environ.get('url_name_country', None)
    region_list = []
    country_dict = {}
    data_fame = None
    base_dir = os.getcwd()

    def get_regions(self):
        headers = {
            "x-rapidapi-host": "restcountries-v1.p.rapidapi.com",
            "x-rapidapi-key": "5ff1b46554msh2c8dc7be94c5f65p15c71ejsne0f18e1d9dd1"
        }
        response = requests.get(url=self.url_countries, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            for data_json in json_response:
                if data_json['region'] not in self.region_list and data_json['region'] != "":
                    self.region_list.append(data_json['region'])
        return self.region_list

    def get_country(self):
        for region in self.get_regions():
            response = requests.get(url=f"{self.url_country}{region}")
            if response.status_code == 200:
                json_response = response.json()
                for data_json in json_response:
                    self.country_dict.update(
                        {region: {'City Name': data_json['name']}}
                    )
                    break
        return self.country_dict

    def get_language_sha1(self):
        data_dict = self.get_country()
        list_result = []
        for region in data_dict:
            start_time = datetime.now()
            country = data_dict[region]
            response = requests.get(url=f"{self.url_name_country}{country['City Name']}")
            if response.status_code == 200:
                json_response = response.json()
                for data_json in json_response:
                    country.update(
                        {'Languaje': str(
                            hashlib.sha1(data_json['languages'][0]['iso639_1'].encode()).hexdigest()).upper(),
                         'Region': region, 'Time': (datetime.now() - start_time).microseconds
                         }
                    )
            list_result.append(country)
        return list_result

    def get_data_frame(self):
        self.data_fame = pd.DataFrame(
            self.get_language_sha1(), columns=['Region', 'City Name', 'Languaje', 'Time']
        )
        print(self.data_fame, flush=True)
        return self.data_fame

    def get_data_time(self):
        self.get_data_frame()
        print('TIEMPO TOTAL = ', self.data_fame['Time'].sum(), flush=True)
        print('TIEMPO PROMEDIO = ', self.data_fame['Time'].mean(), flush=True)
        print('TIEMPO MINIMO = ', self.data_fame['Time'].min(), flush=True)
        print('TIEMPO MAXIMO = ', self.data_fame['Time'].max(), flush=True)

    def save_json_file(self):
        self.get_data_frame().to_json(f"{self.base_dir}/{os.environ.get('json_file', None)}")

    def save_sqlite(self):
        file_name = f"{self.base_dir}/{os.environ.get('sqlite_file', None)}"
        con = sqlite3.connect(f"{file_name}")
        self.get_data_frame().to_sql(name='data', con=con, if_exists="replace")


TestZinobe().save_sqlite()
