import time
import re
from csv import reader
import requests

from django.core.management.base import BaseCommand
from main.models import Confirmed
from main.models import Deaths
import pycountry as pc
from pycountry_convert import country_name_to_country_alpha2

class Command(BaseCommand):
    help = 'Fetches JHU data via the Github API'

    def handle(self, *args, **kwargs):
        def country_code(country):
            # countries that have different names in pycountry
            ccs = {
                'Mainland China': 'cn',
                'UK': 'gb',
                'Korea, South': 'kr',
                'Taiwan*': 'tw',
                'US': 'us',
                'Iran': 'ir',
                'Vietnam': 'vn',
                'Macau': 'mo',
                'Russia': 'ru',
                'Holy See': 'va',
                'Republic of Ireland': 'ie',
                'Moldova': 'md',
                'Czech Republic': 'cz',
                'Saint Barthelemy': 'bl',
                'Palestine': 'ps',
                'Bolivia': 'bo',
                'Cote d\'Ivoire': 'ci',
                'Venezuela': 've',
                'Kosovo': 'xk',
                'Congo (Kinshasa)': 'cd',
                'Congo (Brazzaville)': 'cg',
                'Tanzania': 'tz',
                'Gambia, The': 'gm',
                'Bahamas, The': 'bs',
                'Cape Verde': 'cv',
                'East Timor': 'tp',
                'Brunei': 'bn',
            }
            if pc.countries.get(name=country) is None:
                cc =  '00' if country not in ccs else ccs[country]
            else:
                cc = country_name_to_country_alpha2(country).lower()
            return cc

        def update_database(url_base, file_name, model):
            print('Updating Database for {}...'.format(file_name))
            url = url_base + file_name
            time.sleep(1)
            r = requests.get(url=url, headers={'Accept': 'application/vnd.github.VERSION.raw'})
            data = r.text.splitlines() # re.split('\r', r.text)

            # indexes
            PROVINCE = 0
            COUNTRY = 1
            LAT = 2
            LONG = 3
            CASES = -1

            # add data to database
            # exclude data[0] as those are the labels
            for row in reader(data[1:], delimiter=',', quotechar='"'):
                # if record exists
                if model.objects.filter(province=row[PROVINCE], country=row[COUNTRY]).exists():
                    c = model.objects.get(province=row[PROVINCE], country=row[COUNTRY])
                    try:
                        curr_num_cases = int(row[CASES])
                    except ValueError:
                        curr_num_cases = 0
                    if c.num_cases != curr_num_cases:  # if num_cases in record is outdated
                        c.num_cases = curr_num_cases
                        print('   updated: {}, {}: {}'.format(row[PROVINCE], row[COUNTRY], row[CASES]))
                        c.save()
                else:  # create a new object and save it to the database  
                    if int(row[CASES]) > 0:
                        c = model.objects.create(
                            province=row[PROVINCE],
                            country=row[COUNTRY],
                            country_code=country_code(row[COUNTRY]),
                            latitude=row[LAT],
                            longitude=row[LONG],
                            num_cases=row[CASES])
                        print('created: {}, {}'.format(row[PROVINCE], row[COUNTRY]))
                        c.save()
            print('Database for {} has been updated!!!'.format(file_name))

        url_base = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_time_series/'
        file_names = {
            'time_series_19-covid-Confirmed.csv': Confirmed,
            'time_series_19-covid-Deaths.csv': Deaths
            }

        for file_name, model in file_names.items():
            update_database(url_base, file_name, model)
