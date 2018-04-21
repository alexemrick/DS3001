import tbapy
import pandas as pd
import json
import numpy as np
tba = tbapy.TBA('az3CfBMqtHsElcAwN9pdsjAlIVVHUTCcVPjYRBjPnCQOFqwZ6y9raUnmXXOhQiP7')

# ######################GET WINS, LOSSES, TIES, and TOTAL RANKING POINTS#################################
# all_teams = pd.read_csv('all_teams.csv')
# events = pd.read_csv('2018events.csv')
# events = events['event_code'].values
# events = events
# #events = map(eval, events)
# statistics = pd.DataFrame()
# for event in events:
#     print(event)
#     event_ranking = tba.event_rankings(event)
#     event_ranking = json.dumps(event_ranking, indent=4, sort_keys=True)
#     # print (event_ranking[1])
#
#     obj = json.loads(event_ranking)
#     keys = obj.keys()
#     # print(keys)
#     # print(obj['sort_order_info'])
#
#     parkPoints =  1
#     autoPoints = 2
#     ownershipPoints = 3
#     vaultPoints = 4
#
#     all_ranks = obj['rankings']
#     #print(all_ranks[1]['sort_orders'][1])
#     # print (len(obj['rankings']))
#     # rankings = json.loads(obj['rankings'])
#     # print (rankings.keys())
#
#
#     """
#     What Tom wants: losses, wins, ties and the extra stats number
#     """
#     all_losses = []
#     all_wins = []
#     all_ties = []
#     all_team_key = []
#     all_extra_stats_no = []
#     all_park = []
#     all_auto = []
#     all_ownership = []
#     all_vault = []
#     try:
#         for objects in all_ranks:
#             # print (objects['team_key'])
#             # print (objects['team_key'])
#             all_team_key.append(objects['team_key'])
#             all_extra_stats_no.append(objects['extra_stats'][0])
#             all_wins.append(objects['record']['wins'])
#             all_losses.append(objects['record']['losses'])
#             all_ties.append(objects['record']['ties'])
#             try:
#                 all_park.append(objects['sort_orders'][parkPoints])
#                 all_auto.append(objects['sort_orders'][autoPoints])
#                 all_ownership.append(objects['sort_orders'][ownershipPoints])
#                 all_vault.append(objects['sort_orders'][vaultPoints])
#             except IndexError:
#                 pass
#         # print (all_team_key)
#         #print(all_extra_stats_no)
#         # print (all_wins)
#         # print (all_ties)
#         # print (all_losses)
#
#         df = pd.DataFrame(
#             {'TeamKey': all_team_key,
#              'RankingPoints': all_extra_stats_no,
#              'Wins': all_wins,
#              'Losses': all_losses,
#              'Ties': all_ties,
#              "ClimbPoints": all_park,
#              "AutoPoints": all_auto,
#              "OwnershipPoints": all_ownership,
#              "VaultPoints": all_vault
#             }, columns=["TeamKey","RankingPoints","Wins","Losses","Ties", "ClimbPoints","AutoPoints","OwnershipPoints","VaultPoints"])
#         df = df.sort_values("RankingPoints", ascending=False)
#         statistics = pd.concat([statistics, df])
#     except TypeError:
#         pass
#
# print(statistics)
# statistics.to_csv("TeamStatistics.csv", index=False )

statistics = pd.read_csv('TeamStatistics.csv')
statistics = statistics.groupby(["TeamKey"]).mean()
teams = pd.read_csv('all_teams.csv')
teams = teams.set_index('key')
teams = teams.join(statistics)
teams = teams.dropna()
teams.to_csv("all_data.csv")



