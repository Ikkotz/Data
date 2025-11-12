# main.py
from utils import calculate_correlation, save_and_show
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from nba_api.stats.endpoints import LeagueLeaders, playercareerstats
from nba_api.stats.endpoints.alltimeleadersgrids import AllTimeLeadersGrids
from nba_api.stats.static import players

# 0. Crear el directorio
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs("images", exist_ok=True)

# 1. Descarga de Dataframes
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
df_final.to_csv(os.path.join(DATA_DIR, "Lideres_historicos_ordenado.csv"), index=False, encoding="utf-8-sig")
print("✅ Archivo 'Lideres_historicos_ordenado.csv' creado correctamente.")

# 2. League Leaders
league_leaders = LeagueLeaders(season='2024-25', per_mode48='Totals')
lideres = league_leaders.get_data_frames()[0]
lideres.to_csv(os.path.join(DATA_DIR, "Lideres_de_la_liga.csv"), index=False, encoding="utf-8-sig")
print("✅ Data importada a 'Lideres_de_la_liga.csv'")

lideres_df = lideres.head(200)

# 3. Top 10 FG% 
top10_fg_pct = lideres_df[["PLAYER", "FG_PCT"]].sort_values(by="FG_PCT", ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top10_fg_pct["PLAYER"], top10_fg_pct["FG_PCT"], color="skyblue")
plt.title("Top 10 jugadores por FG%")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
save_and_show("top10_fg_pct.png")

# 4. Top 10 FG3% 
top10_fg3_pct = lideres_df[["PLAYER", "FG3_PCT"]].sort_values(by="FG3_PCT", ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top10_fg3_pct["PLAYER"], top10_fg3_pct["FG3_PCT"], color="skyblue")
plt.title("Top 10 jugadores por FG3%")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
save_and_show("top10_fg3_pct.png")

# 5. Top 10 Asistencias 
top10_ast = lideres_df[["PLAYER", "AST"]].sort_values(by="AST", ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top10_ast["PLAYER"], top10_ast["AST"], color="skyblue")
plt.title("Top 10 Asistencias", fontsize=16)
plt.xlabel("Jugador")
plt.ylabel("Asistencias Totales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Destacar LeBron / Jokic
for label in plt.gca().get_xticklabels():
    if "LeBron" in label.get_text() or "Jokic" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
save_and_show("top10_ast.png")

# 6. Top 10 Rebotes 
top10_reb = lideres_df[["PLAYER", "REB"]].sort_values(by="REB", ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top10_reb["PLAYER"], top10_reb["REB"], color="skyblue")
plt.title("Top 10 Rebotes", fontsize=16)
plt.xlabel("Jugador")
plt.ylabel("Rebotes Totales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
save_and_show("top10_reb.png")

# 7. Puntos de la carrera de LeBron por temporada
lebron = [p for p in players.get_players() if p["full_name"] == "LeBron James"][0]
career_stats = playercareerstats.PlayerCareerStats(player_id=lebron["id"]).get_data_frames()[0]
df_season = career_stats[career_stats["SEASON_ID"] != "Career"]

plt.figure(figsize=(10, 6))
plt.plot(df_season["SEASON_ID"], df_season["PTS"], marker="o")
plt.title("LeBron James - Puntos por Temporada")
plt.xlabel("Temporada")
plt.ylabel("PTS Promedio")
plt.xticks(rotation=45)
save_and_show("lebron_puntos_por_temporada.png")

# 8. LeBron vs otros jugadores (PTS, AST, STL)
# Puntos
all_time_points = {"LeBron James": 42184, "Kareem Abdul-Jabbar": 38387, "Karl Malone": 36928}
plt.bar(all_time_points.keys(), all_time_points.values(), color=["gold", "grey", "brown"])
plt.title("Líderes Históricos en Puntos Totales")
save_and_show("lebron_vs_otros_PTS.png")

# Asistencias
all_time_asis = {"John Stockton": 15806, "Chris Paul": 12528, "Jason Kidd": 12091, "LeBron James": 11584}
plt.bar(all_time_asis.keys(), all_time_asis.values(), color=["blue", "grey", "brown", "gold"])
plt.title("Líderes Históricos en Asistencias Totales")
save_and_show("lebron_vs_otros_AST.png")

# Robos 
all_time_stl = {"John Stockton": 3265, "Chris Paul": 2726, "LeBron James": 2345}
plt.bar(all_time_stl.keys(), all_time_stl.values(), color=["blue", "grey", "gold"])
plt.title("Líderes Históricos en Robos Totales")
save_and_show("lebron_vs_otros_STL.png")

# 9. LeBron en el ranking Historico 
historicos = pd.read_csv(os.path.join(DATA_DIR, "Lideres_historicos_ordenado.csv"))
lebron_historico = historicos[historicos["PLAYER_NAME"] == "LeBron James"]
lebron_historico[["PLAYER_NAME", "RANK", "CATEGORY"]]

plt.figure(figsize=(10, 6))
plt.plot(lebron_historico["CATEGORY"], lebron_historico["RANK"], marker="o")
plt.title("LeBron James - Ranking Historico NBA")
plt.xlabel("Categoría")
plt.ylabel("Ranking (menor es mejor)")
plt.xticks(rotation=45)
plt.gca().invert_yaxis()
save_and_show("lebron_ranking_historico_NBA.png")

# Version Seaborn 
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.lineplot(data=lebron_historico, x="CATEGORY", y="RANK", marker="o", color="royalblue", linewidth=2.5)
plt.title("🏀 LeBron James - Ranking Historico NBA", fontsize=14, fontweight="bold")
plt.xlabel("Categoria")
plt.ylabel("Ranking (más bajo es mejor)")
plt.gca().invert_yaxis()
sns.despine()
plt.tight_layout()
save_and_show("lebron_ranking_historico_NBA.png")

# 10. Jugadores activos vs innactivos
historicos[historicos["IS_ACTIVE_FLAG"] == "Y"].value_counts

historicos_activos = historicos[historicos["IS_ACTIVE_FLAG"] == "Y"]

status_counts = historicos["IS_ACTIVE_FLAG"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(status_counts, labels=["Inactive", "Active"], autopct="%1.1f%%", colors=["grey", "green"])
plt.title("Jugadores Activos vs Retirados")
save_and_show("activos_vs_retirados_pie.png")

# 11. Tiros anotados por Lebron vs Puestos de mecanicos en Carolina del Norte
array_1 = np.array([622,795,875,772,794,789,768,758,621,765,767,624,737,736,857,558,643,422,640,609])
array_2 = np.array([3180,3910,4140,4160,3670,3490,3140,2680,2690,2750,3060,2820,3300,3120,3730,2880,2680,2090,2590,2330])
years = np.arange(2003, 2023)
correlation, r_squared, p_value = calculate_correlation(array_1, array_2)

fig, ax1 = plt.subplots(figsize=(9, 6))
ax1.plot(years, array_1, "k--", marker="d", label="Tiros de LeBron")
ax2 = ax1.twinx()
ax2.plot(years, array_2, "r-", marker="o", label="Mecánicos en Carolina del Norte")
plt.title("Correlación: Tiros anotados por LeBron vs Numero de mecánicos en Carolina del Norte")
plt.figtext(0.13, 0.02, f"r={correlation:.3f}, r²={r_squared:.3f}, p={p_value:.3e}", fontsize=8, color="gray")
fig.tight_layout()
save_and_show("lebron_vs_mechanicos.png")

print("✅ All tasks complete.")