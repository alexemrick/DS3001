import tbapy
import pandas as pd
import json

tba = tbapy.TBA("az3CfBMqtHsElcAwN9pdsjAlIVVHUTCcVPjYRBjPnCQOFqwZ6y9raUnmXXOhQiP7")
wpi = tba.event_teams("2018mawor")
wpi = json.dumps(wpi)
wpi = pd.read_json()
print wpi.head(5)
