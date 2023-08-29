from vk_ads_methods import get_clients, get_campaigns, get_ads, get_statistics
import json
import pandas as pd


with open('assets/clients.json', 'r') as file:
    clients = json.load(file)['response']


# string_of_campaigns_ids = "1023906634, 1024166909, 1027398237, 1028428065, 1028637401, 1028834159"


for client in clients:
    if client['id'] == 1607696736:
        client_id = client['id']
        client_name = client['name']

        campaigns = get_campaigns(client_id=client_id)

        with open('assets/campaigns.json', 'w') as f:
            json.dump(campaigns, f, indent=3)

        list_of_campaigns_ids = [str(i['id']) for i in campaigns['response']]
        string_of_campaigns_ids = ', '.join(list_of_campaigns_ids)

        campaigns_statistics = get_statistics(ids_type="campaign", ids=string_of_campaigns_ids, date_from="2023-08-01", date_to="2023-08-31")

        with open('assets/campaigns_statistics.json', 'w') as f:
            json.dump(campaigns_statistics, f, indent=3)

        df = pd.json_normalize(campaigns_statistics['response'], 'stats', ['id', 'type'])
        json_df = pd.DataFrame(campaigns['response'])
        df = pd.merge(df, json_df[['id', 'name']], on='id', how='left')
        df.to_csv('assets/campaigns_statistics.csv', index=False)

        # ads = get_ads(client_id=client_id, campaign_ids=string_of_campaigns_ids)
        #
        # with open('assets/ads.json', 'w') as f:
        #     json.dump(ads, f, indent=3)
