import pandas as pd

from nba_api.stats.endpoints import playercareerstats
# Nikola Jokić's career stats
career = playercareerstats.PlayerCareerStats(player_id='203999')
print(career)
# Get data as a pandas DataFrame
career_df = career.get_data_frames()[0]
# Get data as JSON
career_json = career.get_json()
# Get data as a dictionary
career_dict = career.get_dict()

from nba_api.live.nba.endpoints import scoreboard
# Today's Score Board
games = scoreboard.ScoreBoard()
print(games)
# Get data as JSON
games_json = games.get_json()
print(games_json)
# Get data as a dictionary
games_dict = games.get_dict()
print(games_dict)