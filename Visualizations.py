import pandas
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, HTML
from gmplot import gmplot
import gmaps
import gmaps.datasets
import gmaps.datasets
import tbapy
import json
%matplotlib inline  

tba = tbapy.TBA('az3CfBMqtHsElcAwN9pdsjAlIVVHUTCcVPjYRBjPnCQOFqwZ6y9raUnmXXOhQiP7')
gmaps.configure(api_key='AIzaSyANJiID5KLBVzBS0molpB6BCkSQOVhIKDM')

figure_US = {
'width': '1000px',
'height': '600px',
'border': '1px solid black',
'padding': '1px'
}

#['Alaska', 66.0685, -152.2782]
#['Hawaii', 21.094318, -157.498337]

stateCoords = [['Alabama', 32.806671, -86.791130], ['Arizona', 34.729759, -111.431221], 
              ['Arkansas', 34.969704, -92.373123], ['California', 36.116203, -119.681564], ['Colorado', 39.059811, -105.311104], 
              ['Connecticut', 41.597782, -72.755371], ['Delaware', 38.989, -75.507141], ['Florida', 27.766279, -81.686783],
              ['Georgia', 33.040619, -83.643074], ['Idaho', 44.240459, -114.478828],
              ['Illinois', 40.349457, -88.986137], ['Indiana', 39.849426, -86.258278], ['Iowa', 42.011539, -93.210526],
              ['Kansas', 38.526600, -97.626486], ['Kentucky', 37.668140, -84.670067], ['Louisiana', 31.169546, -92.367805],
              ['Maine', 45.393947, -69.081927], ['Maryland', 39.063946, -76.802101], ['Massachusetts', 42.230171, -71.530106],
              ['Michigan', 43.326618, -84.536095], ['Minnesota', 45.694454, -94.300192], ['Mississippi', 32.741646, -89.678696],
              ['Missouri', 38.456085, -92.288368], ['Montana', 46.921925, -109.454353], ['Nebraska', 41.325370, -98.868082],
              ['Nevada', 39.813515, -117.055374], ['New Hampshire', 43.452492, -71.563896], ['New Jersey', 40.298904, -74.521011],
              ['New Mexico', 34.840515, -106.248482], ['New York', 43.165726, -74.948051], ['North Carolina', 35.630066, -79.006419],
              ['North Dakota', 47.528912, -99.784012], ['Ohio', 40.388783, -82.764915], ['Oklahoma', 35.565342, -96.928917],
              ['Oregon', 43.872021, -120.870938], ['Pennsylvania', 40.590752, -77.209755], ['Rhode Island', 41.680893, -71.511780],
              ['South Carolina', 33.856892, -80.945007], ['South Dakota', 44.299782, -99.438828], ['Tennessee', 35.747845, -86.692345],
              ['Texas', 31.054487, -98.863461], ['Utah', 40.150032, -111.862434], ['Vermont', 44.045876, -72.710686],
              ['Virginia', 37.769337, -78.169968], ['Washington', 47.400902, -121.490494], ['West Virginia', 38.491226, -80.954453],
              ['Wisconsin', 44.268543, -89.616508], ['Wyoming', 42.755966, -107.302490]]

values = [10, 20, 40, 25, 15, 7, 30, 22, 12, 9, 10, 20, 40, 25, 15, 7, 30, 22, 12, 9, 10, 20, 40, 25, 15, 7, 30, 22, 12, 9,
         10, 20, 40, 25, 15, 7, 30, 22, 12, 9, 10, 20, 40, 25, 15, 7, 30, 22, 12, 9]

allData = pandas.read_csv("all_data.csv")
champs = pandas.read_csv("champsTeams.csv")
states = pandas.DataFrame( allData["state_prov"])
states = states.rename(index=str, columns={"state_prov": "State"})
champs = champs.rename(index=str, columns={"state_prov": "State"})
# print(states)

#group the data by state and get the count
state2 = pandas.DataFrame({'count' : states.groupby( ["State"] ).size()})
champs2 = pandas.DataFrame({'champ count': champs.groupby(["State"]).size()})

# display(HTML(state2.to_html()))
print(champs2)


data = pandas.DataFrame(stateCoords, columns=['State', 'Latitude', 'Longitude'])
data = data.set_index('State')

# display(HTML(data.to_html()))

value = pandas.DataFrame(values, columns=['Size'])
result = data.join(state2)
result = result.join(champs2)
result = result.fillna(0)

display(HTML(result.to_html()))

fig = gmaps.figure(layout = figure_US)

maxNum = result['champ count'].max()

for index, row in result.iterrows():
    
    location = pandas.DataFrame([[row[0], row[1]]])
    
    size = int(row[2] / 5)
    if size == 0:
        size = 1
        
    champ = row[3]
    newValue = int((champ * 255) / maxNum)
    
    r = newValue
    g = 0
    b = 255 - newValue

    string1 = ('rgba(%d, %d, %d, 0.7)'% (r, g, b))
    string2 = ('rgba(%d, %d, %d, 0)'% (r, g, b))
    
    kfc_layer = gmaps.symbol_layer(
        location, fill_color=string1,
        stroke_color=string2, scale=size
    )
    
    
    fig.add_layer(kfc_layer)
    
fig

event_ranking = tba.event_rankings('2018miket')
event_ranking = json.dumps(event_ranking, indent=4, sort_keys=True)
# print (event_ranking[1])

obj = json.loads(event_ranking)
keys = obj.keys()
# print (obj)
all_ranks = obj['rankings']

all_losses = []
all_wins = []
all_ties = []
all_team_key = []
all_extra_stats_no = []

for objects in all_ranks:
    # print (objects['team_key'])
    # print (objects['team_key'])
    all_team_key.append(objects['team_key'])
    all_extra_stats_no.append(objects['extra_stats'][0])
    all_wins.append(objects['record']['wins'])
    all_losses.append(objects['record']['losses'])
    all_ties.append(objects['record']['ties'])

# print (all_team_key)
print(all_extra_stats_no)
# print (all_wins)
# print (all_ties)
# print (all_losses)

df = pandas.DataFrame(
    np.column_stack([all_extra_stats_no, all_wins, all_losses, all_ties]),
     index = all_team_key,
     columns = ['Ranking Points', 'Wins', 'Losses', 'Ties']
    )
print(df)
df.to_csv("TeamStatistics.csv", index=False)

# generate random matrix
num_rows = 500
num_cols = 10
np.random.seed(seed=100)
mat = np.random.rand(num_rows, num_cols)

# make row and col labels
rows = range(num_rows)
cols = range(num_cols)
rows = [str(i) for i in rows]
cols = [str(i) for i in cols]

# make dataframe 
# df = pandas.DataFrame(data=mat, columns=cols, index=rows)

net.load_df(df[['Ranking Points', 'Losses', 'Ties', 'Wins']])
net.cluster(enrichrgram=False)
net.widget()
