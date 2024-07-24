from ballchaser.client import BallChaser
import config
import os
import time
import requests
import ast

API_KEY = config.api_key
BASE_URL = 'https://ballchasing.com/api'
ball_chaser = BallChaser(config.api_key)
save_path = r'D:\all_programming\rlcs-player-analysis\rlcs_2024_replays'
group_id_list = ['rlcs-2024-jsvrszynst']

def Obtain_group_id(group_id_list):
    ticker = 0
    
    for id in group_id_list:
        ticker +=1
    
        try:
            group = list(ball_chaser.list_groups(group_id = id))
        except:
            print('Short error init')
            time.sleep(120)
            group = list(ball_chaser.list_groups(group_id = id))
    
        if len(group) != 0:
            for item in group:
                group_id_list.append(item['id'])
        
        if ticker % 20 == 0:
            print(f'{len(group_id_list)} | {ticker}')

        time.sleep(5)
    return group_id_list

# Function to get group details
def get_group_details(group_id, player_name, player_id):
        # Set headers for API requests
    headers = {
        'Authorization': API_KEY,
    }

    url = f'{BASE_URL}/replays?player-name={player_name}&player-id=steam:{player_id}&group={group_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to get details for group : {response.status_code}')
    return None

def Replay_id_collector(id_array):
    ticker = 0
    replay_id_list = []

    for subgroup_id in id_array:

        time.sleep(5)  # Adjust the delay as necessary
        try:
            group_info = ball_chaser.get_group(subgroup_id)
            print(group_info)
            replay_details = get_group_details(subgroup_id, group_info['players'][0]['name'], group_info['players'][0]['id'])
            if replay_details is not None:
                for replay in replay_details['list']:
                    replay_id_list.append(replay['id'])
            pass
        except:
            print('Base error')
            continue

        ticker += 1
        if ticker % 20 == 0:
            print(f'{len(replay_id_list)} | {ticker}')

        print(len(replay_id_list), ticker)

        # Add a delay to avoid sending too many requests in a short time interval
        

    return replay_id_list

def Replay_downloader(replay_id_list, save_path):
    for replay_data in replay_id_list:
        print(replay_data)
        ball_chaser.download_replay(replay_data, save_path)
        time.sleep(5)

g_id_list = Obtain_group_id(group_id_list)
print('Phase 1 Complete')

r_id_list = Replay_id_collector(g_id_list)
print('Phase 2 Complete')

with open(r'D:\all_programming\rlcs-player-analysis\replaystuff.txt', 'r') as file:
    content = file.read()

r_id_array = ast.literal_eval(content)
Replay_downloader(r_id_array, save_path)
print('Phase 3 Complete')
