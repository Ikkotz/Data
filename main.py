from utils import career, career_df,games_dict,career_json,games,games_json,games_dict, calculate_correlation
import pandas as pd
import json
from nba_api.stats.endpoints import LeagueLeaders
from nba_api.stats.endpoints.alltimeleadersgrids import AllTimeLeadersGrids
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

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
    season = '2024-25', # Se puede cambiar dependiendo del año.
    per_mode48 = 'Totals', # "Totals", "Per48", "PerGame"
    )
lideres = league_leaders.get_data_frames()[0]
lideres.to_csv("Lideres de la liga.csv", index=False, encoding="utf-8-sig")
print("✅ Data importada a Lideres de la liga.csv") 

lideres_df = lideres.head(200) 

lideres_fg_pct = lideres_df[["PLAYER", "FG_PCT"]]
lideres_fg_pct = lideres_fg_pct.sort_values(by="FG_PCT", ascending=False)
top10_fg_pct = lideres_fg_pct.head(10)

print(top10_fg_pct)

top10_fg_pct = lideres_fg_pct.head(10)

plt.figure(figsize=(10, 6))
plt.bar(top10_fg_pct["PLAYER"], top10_fg_pct["FG_PCT"], color="skyblue")
plt.title("Top 10 jugadores por FG%", fontsize=16)
plt.xlabel("Jugador", fontsize=12)
plt.ylabel("FG%", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
plt.close()
plt.savefig("top10_fg_pct.png", dpi=300, bbox_inches="tight")

lideres_df = lideres[0] 
lideres_df = lideres_df.head(200) 

lideres_fg3_pct = lideres_df[["PLAYER", "FG3_PCT"]]
lideres_fg3_pct = lideres_fg3_pct.sort_values(by="FG3_PCT", ascending=False)
top10_fg3_pct = lideres_fg3_pct.head(10)

print(top10_fg3_pct)


plt.figure(figsize=(10, 6))
plt.bar(top10_fg3_pct["PLAYER"], top10_fg3_pct["FG3_PCT"], color="skyblue")
plt.title("Top 10 jugadores por FG3%", fontsize=16)
plt.xlabel("Jugador", fontsize=12)
plt.ylabel("FG%", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()


for label in plt.gca().get_xticklabels():
    if "Zach LaVine" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
    elif "Luke Kennard" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
    elif "Keon Ellis" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
    elif "Grayson Allen" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
plt.show()
plt.savefig()
plt.close()

lideres_ast = lideres_df[["PLAYER", "AST"]]
lideres_ast = lideres_ast.sort_values(ascending=False, by="AST")
lideres_ast[:10]

top10_ast = lideres_ast.head(10)

plt.figure(figsize=(10, 6))
plt.bar(top10_ast["PLAYER"], top10_ast["AST"], color="skyblue")
plt.title("Top 10 Asistencias", fontsize=16)
plt.xlabel("Jugador", fontsize=12)
plt.ylabel("Rebotes Totales", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()


for label in plt.gca().get_xticklabels():
    if "Nikola Jokic" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
    elif "LeBron James" in label.get_text():
        label.set_color("red")
        label.set_fontweight("bold")
plt.show()
plt.savefig()
plt.close()

lideres_reb = lideres_df[["PLAYER", "REB"]]
lideres_reb = lideres_reb.sort_values(ascending=False, by="REB")
lideres_reb[:10],

top10_reb = lideres_reb.head(10)

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(top10_reb["PLAYER"], top10_reb["REB"], color="skyblue")
plt.title("Top 10 Rebotes", fontsize=16)
plt.xlabel("Jugador", fontsize=12)
plt.ylabel("Rebotes", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
plt.savefig()
plt.close()

# LeBron James' player ID
lebron = [player for player in players.get_players() if player['full_name'] == "LeBron James"][0]
lebron_id = lebron['id']

# estadisticas de carrera
career_stats = playercareerstats.PlayerCareerStats(player_id=lebron_id)
df = career_stats.get_data_frames()[0]
print(df.head())


# Averages de Lebron
career_averages = df[df['SEASON_ID'] == 'Career'][['PTS', 'REB', 'AST']]
print("LeBron's Career Averages:")
print(career_averages)

# Puntos de Lebron por temporada
df_season = df[df['SEASON_ID'] != 'Career']
plt.plot(df_season['SEASON_ID'], df_season['PTS'], marker='o')
plt.title("LeBron James Points Per Season")
plt.xlabel("Season")
plt.ylabel("Points Per Game")
plt.xticks(rotation=45)
plt.show()
plt.savefig()
plt.close()

# Lebron VS otros jugadores
all_time_points = {'LeBron James': 42184, 'Kareem Abdul-Jabbar': 38387, 'Karl Malone': 36928}
players = list(all_time_points.keys())
points = list(all_time_points.values())

plt.bar(players, points, color=['yellow', 'grey', 'brown'])
plt.title("Lideres Hitoricos")
plt.ylabel("Puntos Totales")
plt.show()
plt.savefig()
plt.close()

# Lebron VS otros jugadores
all_time_asis = {'John Stockton': 15806, 'Chris Paul': 12528, 'Jason Kidd': 12091 ,'LeBron James': 11584}
players = list(all_time_asis.keys())
points = list(all_time_asis.values())

plt.bar(players, points, color=['yellow', 'grey', 'brown'])
plt.title("Lideres Hitoricos")
plt.ylabel("Asistencias Totales")
plt.show()
plt.savefig()
plt.close()

# Lebron VS otros jugadores
all_time_stl = {'John Stockton': 3265, 'Chris Paul': 2726,'LeBron James': 2345}
players = list(all_time_stl.keys())
points = list(all_time_stl.values())

plt.bar(players, points, color=['yellow', 'grey', 'brown'])
plt.title("Lideres Historicos")
plt.ylabel("Robos Totales")
plt.show()
plt.savefig()
plt.close()


historicos = pd.read_csv("Lideres_historicos_ordenado.csv")

lebron_historico = historicos[historicos["PLAYER_NAME"] == "LeBron James"]

lebron_historico[["PLAYER_NAME", "RANK", "CATEGORY"]]

plt.plot(lebron_historico['CATEGORY'], lebron_historico['RANK'], marker='o')
plt.title("LeBron James Rank ALL TIME per Category")
plt.xlabel("CATEGORY")
plt.ylabel("RANK")
plt.xticks(rotation=45)

plt.gca().invert_yaxis()
plt.show()
plt.savefig()
plt.close()


# Estilo general
sns.set_theme(style="whitegrid")

plt.figure(figsize=(10,6))
sns.lineplot(
    data=lebron_historico,
    x='CATEGORY',
    y='RANK',
    marker='o',
    linewidth=2.5,
    color='royalblue'
)

plt.title("🏀 LeBron James - All-Time Rank per Category", fontsize=14, fontweight='bold')
plt.xlabel("Category", fontsize=12)
plt.ylabel("Rank (lower is better)", fontsize=12)
plt.xticks(rotation=45)
plt.gca().invert_yaxis()  # Mostrar mejores posiciones arriba

sns.despine()
plt.tight_layout()
plt.show()
plt.savefig()
plt.close()

historicos = pd.read_csv("Lideres_historicos_ordenado.csv")
historicos["CATEGORY"].value_counts()
historicos.set_index("RANK")

historicos[historicos["IS_ACTIVE_FLAG"] == "Y"].value_counts

historicos_activos = historicos[historicos["IS_ACTIVE_FLAG"] == "Y"]

status_counts = historicos["IS_ACTIVE_FLAG"].value_counts()

status_counts

plt.figure(figsize=(6, 6))
plt.pie(status_counts, labels=["Inactive", "Active"], autopct='%1.1f%%', colors=["grey", "green"])
plt.title("Active vs Inactive Players")
plt.show()
plt.savefig()
plt.close()

array_1 = np.array([622,795,875,772,794,789,768,758,621,765,767,624,737,736,857,558,643,422,640,609,])
array_2 = np.array([3180,3910,4140,4160,3670,3490,3140,2680,2690,2750,3060,2820,3300,3120,3730,2880,2680,2090,2590,2330,])
array_1_name = "Numero de tiros de Lebron James"
array_2_name = "Numero de mecánicos que cambian y reparan ruedas en Carolina del Norte"
correlation_df = pd.DataFrame({'Numero de tiros de Lebron James': array_1, 'Numero de mecánicos que cambian y reparan ruedas en Carolina del norte': array_2})
print(f"Calcular la correlacion entre {array_1_name} y {array_2_name}...")

calculate_correlation(array_1, array_2)
correlation, r_squared, p_value = calculate_correlation(array_1, array_2)

print("Coeficiente de correlacion:", correlation)
print("R cuadrada:", r_squared)
print("P-value:", p_value)

years = np.arange(2003, 2023)

fig, ax1 = plt.subplots(figsize=(9, 6))

# Lebron
ax1.plot(years, array_1, 'k--', marker='d', label="Numero de tiros de Lebron James")
ax1.set_xlabel('Anyos')
ax1.set_ylabel('Numero de tiros de Lebron James', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Mecanicos
ax2 = ax1.twinx()
ax2.plot(years, array_2, 'r-', marker='o', label="Numero de mecánicos que cambian y reparan ruedas en Carolina del norte")
ax2.set_ylabel('Mecanicos', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Titlulos
plt.title("Numero de tiros de Lebron James", fontsize=14, fontweight='bold', pad=20)
plt.suptitle("Numero de mecánicos que cambian y reparan ruedas en Carolina del Norte", 
             fontsize=13, color='darkred', y=0.94)

# Anotaciones
plt.figtext(0.13, 0.02, 
            "Fuente: Basketball-Reference & Bureau of Labor Statistics",
            fontsize=8, color='gray')

plt.figtext(0.13, 0.00, 
            "2003–2022, r=0.785, r²=0.616, p<0.01 • tylervigen.com/spurious/correlation/2177",
            fontsize=8, color='gray')


fig.tight_layout()

plt.show()
plt.savefig()
plt.close()