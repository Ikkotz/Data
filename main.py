from utils import career, career_df,games_dict,career_json,games,games_json,games_dict
import pandas as pd
import json

from nba_api.stats.endpoints import CommonTeamRoster
from nba_api.stats.endpoints import LeagueLeaders

common_team_roster = CommonTeamRoster(
    team_id = '1610612739', # input team id
    league_id_nullable = '00', # nba 00, g_league 20, wnba 10
    season='2022-23')
df_common_team_roster = common_team_roster.get_data_frames()[0]
df_common_team_roster

df_common_team_roster.to_csv("Team Roster.csv", index=False, encoding="utf-8-sig")
print("✅ Data importada a Team Roster.csv")

league_leaders = LeagueLeaders(
    league_id = '00', # nba 00, g_league 20, wnba 10
    season = '2022-23', # change year(s) if needed
    per_mode48 = 'PerGame', # "Totals", "Per48", "PerGame"
    )
df_league_leaders = league_leaders.get_data_frames()[0]
df_league_leaders.to_csv("Lideres de la liga.csv", index=False, encoding="utf-8-sig")
print("✅ Data importada a Lideres de la liga.csv")

#Hipotesis_
##Lideres de cada categoria es un base para asistencias? Un pivot para rebotes?