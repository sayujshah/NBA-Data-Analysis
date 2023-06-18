from referee_database import ref_lookup

referee = input('Enter referee name: ')
team = input('Enter full team city and name: ')
homeaway = input('Home or Away data? (Enter "Home" or "Away"): ' )

print(ref_lookup(referee, team, homeaway))