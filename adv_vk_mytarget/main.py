from methods import get_campaigns, get_ads, get_campaigns_statistics, get_ads_statistics, load_to_database, convert_to_dataframe
import pandas as pd
import requests
import datetime
import json


client_name = 'adv_hr_belagroprombank_mytarget'
with open('../resources/adv_tokens.json') as json_file:
    data = json.load(json_file)

for i in data:
    if i['client_name'] == client_name:
        access_token = i['access_token']

date_to = datetime.date.today()
date_from = str(datetime.date(date_to.year, date_to.month - 2, 1))


campaigns = get_campaigns(client_name=client_name,
                          access_token=access_token)

campaigns_df = pd.DataFrame(campaigns['items'])
campaigns_dict = {i['id']: i['name'] for i in campaigns['items']}
campaigns_ids = list(campaigns_dict.keys())

campaigns_statistics = get_campaigns_statistics(date_from=date_from,
                                                date_to=str(date_to),
                                                campaigns_ids=campaigns_ids,
                                                client_name=client_name,
                                                access_token=access_token)

df = convert_to_dataframe(statistics=campaigns_statistics,
                          reference_df=campaigns_df,
                          client_name=client_name,
                          category='campaigns')

# load_to_database(df, table_name)


ads = get_ads(client_name=client_name,
              access_token=access_token)

ads_df = pd.DataFrame(ads['items'], columns=['id', 'name', ])
ads_dict = {i['id']: i['name'] for i in ads['items']}
ads_ids = list(ads_dict.keys())

ads_statistics = get_ads_statistics(date_from=date_from,
                                    date_to=str(date_to),
                                    ads_ids=ads_ids,
                                    client_name=client_name,
                                    access_token=access_token)

df = convert_to_dataframe(statistics=ads_statistics,
                          reference_df=ads_df,
                          client_name=client_name,
                          category='ads')

# load_to_database(df, table_name)
