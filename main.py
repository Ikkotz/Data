from utils import career, career_df,games_dict,career_json,games,games_json,games_dict
import pandas as pd
import json
from nba_api.stats.endpoints import LeagueLeaders
from nba_api.stats.endpoints.alltimeleadersgrids import AllTimeLeadersGrids
import pandas as pd

data = AllTimeLeadersGrids()
data_frames = data.get_data_frames()

lista = []

for df in data_frames:
    stat_cols = [c for c in df.columns if c not in ['PLAYER_ID', 'PLAYER_NAME', 'IS_ACTIVE_FLAG'] and not c.endswith('_RANK')]
    rank_cols = [c for c in df.columns if c.endswith('_RANK')]
    
    if not stat_cols or not rank_cols:
        continue  
    
    stat = stat_cols[0]
    rank_col = rank_cols[0]
    
    ordenado = df[['PLAYER_ID', 'PLAYER_NAME', stat, rank_col, 'IS_ACTIVE_FLAG']].copy()
    ordenado.columns = ['PLAYER_ID', 'PLAYER_NAME', 'VALUE', 'RANK', 'IS_ACTIVE_FLAG']
    ordenado['CATEGORY'] = stat
    lista.append(ordenado)

df_final = pd.concat(lista, ignore_index=True)


df_final.to_csv("Lideres_historicos_ordenado.csv", index=False, encoding="utf-8-sig")
print("✅ Archivo 'Lideres_historicos_ordenado.csv' creado correctamente.")


league_leaders = LeagueLeaders(
    league_id = '00', # nba 00, g_league 20, wnba 10
    season = '2022-23', # Se puede cambiar dependiendo del año.
    per_mode48 = 'Totals', # "Totals", "Per48", "PerGame"
    )
df_league_leaders = league_leaders.get_data_frames()[0]
df_league_leaders.to_csv("Lideres de la liga.csv", index=False, encoding="utf-8-sig")
print("✅ Data importada a Lideres de la liga.csv")