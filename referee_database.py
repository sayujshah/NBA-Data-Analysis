import pandas as pd
from collections import Counter
import os

absolute_path = os.path.dirname(os.path.abspath(__file__)) + '\\'

def load_data(file, columns):
    out = pd.read_csv(absolute_path + file)[columns]
    return out

games = load_data('game.csv', ['game_id', 'game_date', 'team_name_home', 'team_name_away', 'wl_home'])
officials = load_data('officials.csv', ['game_id', 'official_id', 'first_name', 'last_name'])

officials['name'] = officials['first_name'] + ' ' + officials['last_name']
officials = officials.drop(['first_name', 'last_name'], axis=1)

officials_outcomes = games.merge(officials, on='game_id', how='left').dropna()

def dict_count(df, homeaway):
    df2 = pd.DataFrame(df.groupby('name')['team_name_' + homeaway].apply(list)).reset_index()
    out = {}

    for index, row in df2.iterrows():
        out[row['name']] = Counter(row['team_name_' + homeaway])

    for key1 in out:
        for key2 in out[key1]:
            out[key1][key2] = {'total games': out[key1][key2]}
    
    for index, row in df.iterrows():
        if row['wl_home'] == 'W':
            if 'W' in list(out[row['name']][row['team_name_' + homeaway]].keys()):
                out[row['name']][row['team_name_' + homeaway]]['W'] += 1
            else:
                out[row['name']][row['team_name_' + homeaway]]['W'] = 1
        else:
            if 'L' in list(out[row['name']][row['team_name_' + homeaway]].keys()):
                out[row['name']][row['team_name_' + homeaway]]['L'] += 1
            else:
                out[row['name']][row['team_name_' + homeaway]]['L'] = 1
    
    return out

ref_home_dict = dict_count(officials_outcomes, 'home')
ref_away_dict = dict_count(officials_outcomes, 'away')

def ref_lookup(referee, team, homeaway):
    if homeaway == 'Home':
        return ref_home_dict[referee][team]
    elif homeaway =='Away':
        return ref_away_dict[referee][team]