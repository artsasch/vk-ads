from methods import get_campaigns, get_ads, get_campaigns_statistics, get_ads_statistics, load_to_database
import pandas as pd
import requests
import datetime
import json


client_id = 17778548
client_name = 'adv_cabandos_vk'
with open('../resources/adv_tokens.json') as json_file:
    data = json.load(json_file)
access_token = data[client_name]['access_token']

date_to = datetime.date.today()
date_from = str(datetime.date(date_to.year, date_to.month - 2, 1))


campaigns = get_campaigns(client_id=client_id,
                          client_name=client_name,
                          access_token=access_token)

campaigns_df = pd.DataFrame(campaigns['items'])
campaigns_dict = {i['id']: i['name'] for i in campaigns['items']}
campaigns_ids = list(campaigns_dict.keys())

campaigns_statistics = get_campaigns_statistics(date_from=date_from,
                                                date_to=str(date_to),
                                                campaigns_ids=campaigns_ids,
                                                client_name=client_name,
                                                access_token=access_token)
table_name = f'{client_name}_campaigns_statistics'

df = pd.json_normalize(campaigns_statistics['items'], 'rows', 'id')
df = pd.merge(df, campaigns_df[['id', 'name']], on='id', how='left')
df.to_csv(f'assets/{table_name}.csv', index=False)
df = pd.read_csv(f'assets/{table_name}.csv')
# # load_to_database(df, client_name)


ads = get_ads(client_id=client_id,
              client_name=client_name,
              access_token=access_token)

ads_df = pd.DataFrame(ads['items'], columns=['id', 'name', ])
ads_dict = {i['id']: i['name'] for i in ads['items']}
ads_ids = list(ads_dict.keys())

ads_statistics = get_ads_statistics(date_from=date_from,
                                    date_to=str(date_to),
                                    ads_ids=ads_ids,
                                    client_name=client_name,
                                    access_token=access_token)
table_name = f'{client_name}_ads_statistics'

df = pd.json_normalize(ads_statistics['items'], 'rows', 'id')
df = pd.merge(df, ads_df[['id', 'name']], on='id', how='left')
df.to_csv(f'assets/{table_name}.csv', index=False)
df = pd.read_csv(f'assets/{table_name}.csv')
# load_to_database(df, client_name)
