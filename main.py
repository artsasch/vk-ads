from vk_ads_methods import get_clients, get_campaigns, get_ads, get_statistics, get_ads_layout
import json
import pandas as pd


with open('assets/clients.json', 'r') as file:
    clients = json.load(file)['response']


for client in clients:
    if client['id'] == 1607696736:
        client_id = client['id']
        client_name = client['name']

        # campaigns
        campaigns = get_campaigns(client_id=client_id)

        with open(f'assets/{client_name}_campaigns.json', 'w') as f:
            json.dump(campaigns, f, indent=3)

        list_of_campaigns_ids = [str(i['id']) for i in campaigns['response']]
        string_of_campaigns_ids = ', '.join(list_of_campaigns_ids)

        campaigns_statistics = get_statistics(ids_type="campaign",
                                              ids=string_of_campaigns_ids,
                                              date_from="2023-08-01",
                                              date_to="2023-08-31")

        df = pd.json_normalize(campaigns_statistics['response'], 'stats', ['id', 'type'])
        json_df = pd.DataFrame(campaigns['response'])
        df = pd.merge(df, json_df[['id', 'name']], on='id', how='left')
        df.to_csv(f'assets/{client_name}_campaigns_statistics.csv', index=False)

        # ads
        ads = get_ads(client_id=client_id, campaign_ids=string_of_campaigns_ids)

        with open(f'assets/{client_name}_ads.json', 'w') as f:
            json.dump(ads, f, indent=3)

        list_of_ads_ids = [str(i['id']) for i in ads['response']]
        string_of_ads_ids = ', '.join(list_of_ads_ids)

        ads_statistics = get_statistics(ids_type="ad",
                                        ids=string_of_ads_ids,
                                        date_from="2023-08-01",
                                        date_to="2023-08-31")

        df = pd.json_normalize(ads_statistics['response'], 'stats', ['id', 'type'])
        json_df = pd.DataFrame(ads['response'])[['id', 'name']]
        df = pd.merge(df, json_df, on='id', how='left')

        ads_layout = get_ads_layout(string_of_ads_ids, client_id=client_id)
        json_df = pd.DataFrame(ads_layout['response'])[['id', 'link_url', 'preview_link']]
        df = pd.merge(df, json_df, on='id', how='left')

        df.to_csv(f'assets/{client_name}_ads_statistics.csv', index=False)
