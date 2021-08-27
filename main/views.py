import json

from django.core import serializers
from django.shortcuts import render
from .models import Confirmed
from .models import Deaths
from decouple import config

# Create your views here.

def homepage(request): 
    def format_data(retrieved_data):
        cases_by_province = {}  # {confirmed, deaths}
        cases_by_country = {}

        for record in retrieved_data:
            fields = record['fields']
            location = '{}, {}'.format(fields['province'], fields['country']) if fields['province'] != '' else fields['country']
            fields.pop('province')
            country = fields.pop('country')
            # only keep track of cases with more than one confirmed case
            # some provinces lose cases as those cases turn into recovered cases
            if location == 'Philippines':
                print('yep')
                print(fields['num_cases'])
            if fields['num_cases'] > 0:
                cases_by_province[location] = fields

            # group by country
            if country not in cases_by_country:
                labels = {'num_cases': fields['num_cases'], 'country_code': fields['country_code']}
                cases_by_country[country] = labels
            else:
                if location == 'Philippines':
                    print('YEPP')
                prev_num_cases = cases_by_country[country]['num_cases']
                labels = {'num_cases': fields['num_cases'] + prev_num_cases, 'country_code': fields['country_code']}
                cases_by_country[country] = labels

        total_cases = sum([cases_by_country[c]['num_cases'] for c in cases_by_country])
        return cases_by_province, cases_by_country, total_cases


    # data from the database
    # https://stackoverflow.com/questions/39390927/convert-model-objects-all-to-json-in-python-using-django
    retrieved_confirmed = json.loads(serializers.serialize('json', Confirmed.objects.all()))
    confirmed_by_province, confirmed_by_country, total_confirmed = format_data(retrieved_confirmed)
    
    retrieved_deaths = json.loads(serializers.serialize('json', Deaths.objects.all()))
    deaths_by_province, deaths_by_country, total_deaths = format_data(retrieved_deaths)

    # combine confirmed_by_country data and deaths_by_country data
    # to make it easier to use in the template
    by_country = {}
    for c in confirmed_by_country.keys():
        by_country[c] = {
            'country_code': confirmed_by_country[c]['country_code'],
            'confirmed_num_cases': confirmed_by_country[c]['num_cases'],
            'deaths_num_cases': 0 if c not in deaths_by_country else deaths_by_country[c]['num_cases']
        }

    by_province = {}
    for p in confirmed_by_province.keys():
        by_province[p] = {
            'longitude': confirmed_by_province[p]['longitude'],
            'latitude': confirmed_by_province[p]['latitude'],
            'confirmed_num_cases': confirmed_by_province[p]['num_cases'],
            'deaths_num_cases': 0 if p not in deaths_by_province else deaths_by_province[p]['num_cases']
        }
         
    return render(
        request=request,
        template_name='main/index.html',
        context={
            'by_province': json.dumps(by_province),
            'by_country': by_country,
            'total_deaths': total_deaths,
            'total_confirmed': total_confirmed,
            'SECRET_KEY': config('SECRET_KEY')  # from .env via python-decouple
        })
