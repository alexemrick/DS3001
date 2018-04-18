import tbapy
import pandas as pd
import json
from datetime import datetime
import numpy

import numpy as np
tba = tbapy.TBA('az3CfBMqtHsElcAwN9pdsjAlIVVHUTCcVPjYRBjPnCQOFqwZ6y9raUnmXXOhQiP7')
###############INITIAL DATA COLLECTION######################
#  teamsList = []
# for i in range(0,20):
#     teams = tba.teams(i)
#     teams = json.dumps(teams)
#     teams = pd.read_json(teams)
#     teamsList.append(teams)
#     i+=1
#
# all_teams = pd.concat(teamsList, ignore_index=True)
# # all_teams = all_teams[:50]
# #print(all_teams.columns.values)
# # # all_teams = all_teams[all_teams["team_number"] <= 7331]

################################ Drop useless columns############################################
# drop_list = ["lat","lng","address", 'city', 'country', 'gmaps_place_id', 'gmaps_url','home_championship', 'location_name', 'motto','name','postal_code','website']
# all_teams = all_teams.drop(drop_list, axis=1)
# # # # all_teams['test'],all_teams['test2']=[0,0]
# # # all_teams['opr'],all_teams['RP'],all_teams['district_points'],all_teams['W-L-T'],all_teams["match_points"] = [0,0,0,0,0]


####################GET ONLY THE TEAMS THAT HAVE PLAYED THIS YEAR#################################
# teamkeys = all_teams['key'].values
# for team in teamkeys:
#     print(team)
#     try:
#         lastActiveYear = tba.team_years(team)[-1]
#     except IndexError:
#         lastActiveYear = 0
#
#     if lastActiveYear != 2018:
#         index = all_teams.index[all_teams['key'] == team].tolist()
#         all_teams = all_teams.drop(index[0])
#
# # all_teams.to_csv("all_teams.csv")
# #
# # all_teams = pd.read_csv('all_teams.csv')
# # print(all_teams)

########################ADD THE EVENTS OF EACH TEAM#################################################################
# eventSeries =[]
# for team in all_teams['key']:
#     print(team)
#     all_events = tba.team_events(team, year=2018)
#     teamEvents = []
#     for event in all_events:
#         code = event['event_code']
#         code = "2018"+str(code)
#         teamEvents.append(code)
#     eventSeries.append(teamEvents)
#
# eventSeries = pd.Series(eventSeries)
# all_teams['events'] = eventSeries
# print(all_teams)
# all_teams.to_csv("all_teams.csv")

########################GET THE AVERAGE ADVANCED STATS OF EACH TEAM
# all_oprs =[]
# all_dprs =[]
# all_ccwms = []
# for team in all_teams['key'].values:
#     advanced_data = []
#     print(team)
#     teamEvents = all_teams[all_teams['key'] == team]['events'].values
#     averageOPR = []
#     averageDPR = []
#     averageCCWM = []
#     for eventList in teamEvents:
#         OPRs = []
#         DPRs = []
#         CCWMs = []
#         for event in eventList:
#             try:
#                 eventData = tba.event_oprs(event)
#                 try:
#                     try:
#                         OPRs.append(eventData.oprs[team])
#                         DPRs.append(eventData.dprs[team])
#                         CCWMs.append(eventData.ccwms[team])
#                     except AttributeError:
#                         print(str(event) + " has bad data")
#                 except KeyError:
#                     #for some reason the team was registered for the event but did'nt go i think
#                     print("Got key error for " + str(team) + "at " + str(event))
#
#             except TypeError:
#                 print("Event hasn't happended yet")
#         try:
#             averageOPR = sum(OPRs)/float(len(OPRs))
#             averageDPR = sum(DPRs) / float(len(DPRs))
#             averageCCWM = sum(CCWMs) / float(len(CCWMs))
#         except ZeroDivisionError:
#             print(team + " has not played any events yet, but are registered for an upcoming one")
#     all_oprs.append(averageOPR)
#     all_dprs.append(averageDPR)
#     all_ccwms.append(averageCCWM)
#
# all_teams['OPR'] = all_oprs
# all_teams['DPR'] = all_dprs
# all_teams['CCWM'] = all_ccwms
# all_teams.to_csv("all_teams.csv")

# #  testTeam = all_teams[:1]
# # print(testTeam)
# # team = testTeam['key']
# # events = list(testTeam['events'].values)
# # print(events[0][0])
# # #get opr
# # print(tba.event("2018miket"))

######################GET WINS, LOSSES, TIES, and TOTAL RANKING POINTS#################################
all_teams = pd.read_csv('all_teams.csv')
events = all_teams['events'].values
events = map(eval, events)
week0Events = tba.events(2018)
week0Events = json.dumps(week0Events)
week0Events = pd.read_json(week0Events)
event_codes = week0Events['event_code']
# event_codes= event_codes.values
end_dates = week0Events['end_date']
# end_dates = end_dates.values
# week0Events = week0Events['event_code', 'end_date']
realEvents = pd.concat([end_dates, event_codes], axis=1)
realEvents.columns = ['end_date', 'event_code']
realEvents['end_date'] = realEvents['end_date'].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True))
week1Start = datetime(2018,2,28)
realEvents = realEvents[realEvents['end_date']>week1Start]
realEvents = realEvents.sort_values(by=['end_date'])
realEvents = realEvents['event_code'].values
all_events = []
for event in realEvents:
    event = "2018"+str(event)
    all_events.append(event)
all_events = pd.DataFrame(all_events)
all_events.columns = ['event_code']
print(all_events)
all_events.to_csv('2018events.csv')
event_ranking = tba.event_rankings('2018miket')
#event_ranking = json.dumps(event_ranking, indent=4, sort_keys=True)
print(event_ranking)
