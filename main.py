from vk_ads_methods import get_clients, get_campaigns, get_ads, get_statistics
import json


# get_clients()
# get_campaigns(client_id=client_id)
# get_ads(client_id=client_id, campaign_ids=campaign_id)
# get_statistics(ids_type="campaign", ids=campaign_id, date_from="2023-08-01", date_to="2023-08-31")


with open('assets/clients.json', 'r') as file:
    clients = json.load(file)['response']

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
        