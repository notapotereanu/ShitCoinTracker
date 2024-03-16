import requests
import json
import time
import pandas as pd

def unpackJson(fileName):
    with open(fileName, 'r', encoding='utf-8') as file:
        parsed_json = json.load(file)
        data_list = parsed_json['data']
        
        return data_list
            
def createDictFromEntry(entry):
    # time.sleep(2) # throling
    url = f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={entry["id"]}&range=1M"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None 

    first_key = list(data['data']['points'].keys())[0]
    first_value_v = data['data']['points'][first_key]['v'][-5]

    last_key = list(data['data']['points'].keys())[-1]
    last_value_v = data['data']['points'][last_key]['v'][-5]

    increaseInLastMonth = (last_value_v - first_value_v) / first_value_v * 100 if first_value_v != 0 else 0  # Added a zero check to avoid division by zero

    dictionary = {
        "id": entry["id"],
        "rank": entry["rank"],
        "symbol": entry["symbol"],
        "firstPrice":  round(first_value_v,2), 
        "lastPrice":  round(last_value_v,2),
        "increaseInLastMonth": round(increaseInLastMonth,2),
        "platform": entry["platform"],
    }

    return dictionary

listaFinale = []
jsonListUnpacked = unpackJson("map.json")
for entry in jsonListUnpacked:
    dic = createDictFromEntry(entry) 
    if dic:  
        listaFinale.append(dic)

listaFinale.sort(key=lambda x: x["increaseInLastMonth"])

df = pd.DataFrame(listaFinale)

df.to_csv("crypto.csv", index=False)