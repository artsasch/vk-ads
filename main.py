from vk_ads_methods import get_clients, get_campaigns, get_ads, get_statistics, get_ads_layout, load_to_database
import json
import pandas as pd
from datetime import datetime


date_to = datetime.now()
date_to_str = date_to.strftime('%Y-%m-%d')
date_from = datetime(date_to.year, date_to.month - 1, 1) if date_to.month > 1 else datetime(date_to.year - 1, 12, 1)
date_from_str = date_from.strftime('%Y-%m-%d')


with open('assets/clients.json', 'r') as file:
    clients = json.load(file)['response']

id_name_dict = {1608343119: "adv_ostrov_chistoti_smm",
                1608327357: "adv_mimimi",
                1607696736: "adv_savushkin"}

for client in clients:
    if client['id'] in [1608343119, 1608327357, 1607696736]:
        client_id = client['id']
        client_name = id_name_dict[client_id]

        # campaigns
        campaigns = get_campaigns(client_id=client_id)

        # with open(f'assets/{client_name}_campaigns.json', 'w') as f:
        #     json.dump(campaigns, f, indent=3)

        list_of_campaigns_ids = [str(i['id']) for i in campaigns['response']]
        string_of_campaigns_ids = ', '.join(list_of_campaigns_ids)

        campaigns_statistics = get_statistics(ids_type="campaign",
                                              ids=string_of_campaigns_ids,
                                              date_from=date_from_str,
                                              date_to=date_to_str)

        table_name = f'{client_name}_campaigns_statistics'.lower()

        df = pd.json_normalize(campaigns_statistics['response'], 'stats', ['id', 'type'])
        json_df = pd.DataFrame(campaigns['response'])
        df = pd.merge(df, json_df[['id', 'name']], on='id', how='left')
        df.to_csv(f'assets/{table_name}.csv', index=False)
        df = pd.read_csv(f'assets/{table_name}.csv')
        load_to_database(df, table_name)

        # ads
        ads = get_ads(client_id=client_id, campaign_ids=string_of_campaigns_ids)

        # with open(f'assets/{client_name}_ads.json', 'w') as f:
        #     json.dump(ads, f, indent=3)

        list_of_ads_ids = [str(i['id']) for i in ads['response']]
        string_of_ads_ids = ', '.join(list_of_ads_ids)

        ads_statistics = get_statistics(ids_type="ad",
                                        ids=string_of_ads_ids,
                                        date_from=date_from_str,
                                        date_to=date_to_str)

        table_name = f'{client_name}_ads_statistics'.lower()

        df = pd.json_normalize(ads_statistics['response'], 'stats', ['id', 'type'])
        json_df = pd.DataFrame(ads['response'])[['id', 'name']]
        df = pd.merge(df, json_df, on='id', how='left')

        ads_layout = get_ads_layout(string_of_ads_ids, client_id=client_id)
        json_df = pd.DataFrame(ads_layout['response'])[['id', 'link_url', 'preview_link']]
        df = pd.merge(df, json_df, on='id', how='left')

        df.to_csv(f'assets/{table_name}.csv', index=False)
        df = pd.read_csv(f'assets/{table_name}.csv')
        load_to_database(df, table_name)
