import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, date
import numpy as np
from dotenv import load_dotenv

load_dotenv()

headers = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

# Helper function to fetch data
def fetch_teams():
    url = "https://api-nba-v1.p.rapidapi.com/teams"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['response']

def fetch_games(season, team_id):
    url = f"https://api-nba-v1.p.rapidapi.com/games?season={season}&team={team_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['response']

def fetch_players(team_id):
    url = f"https://api-nba-v1.p.rapidapi.com/players?team={team_id}&season=2023"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['response']

def fetch_standings(season):
    url = f"https://api-nba-v1.p.rapidapi.com/standings?season={season}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['response']

# Title and Description
st.title('NBA Data Explorer')
st.write('Explore NBA teams, games, and player statistics using the API-NBA API.')
st.image('https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg', caption='NBA Logo')

# Progress Bar (Optional)
progress_bar = st.progress(0)

# Fetch Teams Data
with st.spinner('Loading teams data...'):
    teams = fetch_teams()
    progress_bar.progress(20)

# Interactive Dataframe
st.header('Teams Data')
if st.checkbox('Show Teams Data'):
    teams_df = pd.DataFrame(teams)
    st.dataframe(teams_df)
    st.success('Teams data loaded successfully!')

progress_bar.progress(40)

# Selectbox Widget
st.header('Team Selection')
team_names = [team['name'] for team in teams if team['nbaFranchise'] == True]
selected_team = st.selectbox('Select a team:', team_names)

# Get selected team ID
team_id = next(team['id'] for team in teams if team['name'] == selected_team)

# Date Input Widget
selected_date = st.date_input('Select a date', date.today())

# Button Widget
if st.button('Fetch Games'):
    with st.spinner('Fetching games...'):
        games = fetch_games(season=2022, team_id=team_id)
        progress_bar.progress(60)
        games_on_date = [game for game in games if game['date']['start'].startswith(selected_date.strftime('%Y-%m-%d'))]
        if games_on_date:
            games_df = pd.DataFrame(games_on_date)
            st.dataframe(games_df)
            st.success(f"Found {len(games_on_date)} games on {selected_date.strftime('%Y-%m-%d')}.")
        else:
            st.warning(f"No games found on {selected_date.strftime('%Y-%m-%d')}.")
    progress_bar.progress(80)

# Slider Widget
st.header('Player Statistics')
num_players = st.slider('Select number of players to display', 1, 15, 5)

# Radio Button Widget
stat_choice = st.radio('Select statistic to display:', ('Points', 'Rebounds', 'Assists'))

# Fetch Players Data
with st.spinner('Fetching players data...'):
    players = fetch_players(team_id=team_id)
    progress_bar.progress(90)

players_df = pd.DataFrame(players)

if not players_df.empty:
    # Display top players based on selected statistic
    stat_map = {
        'Points': 'points',
        'Rebounds': 'totReb',
        'Assists': 'assists'
    }
    stat_column = stat_map[stat_choice]
    # For demonstration, we'll create dummy statistics
    players_df[stat_column] = np.random.randint(0, 30, size=len(players_df))
    st.info(f'Displaying top {num_players} players by {stat_choice}')
    top_players = players_df[['firstname', 'lastname', stat_column]].sort_values(by=stat_column, ascending=False).head(num_players)
    st.dataframe(top_players)

    # Bar Chart
    st.subheader('Player Statistics Chart')
    chart_data = top_players.set_index('lastname')[stat_column]
    st.bar_chart(chart_data)

    # Area Chart
    st.subheader('Player Statistics Over Time (Dummy Data)')
    time_data = pd.DataFrame({
        'Game': range(1, 11),
        stat_choice: np.random.randint(0, 30, size=10)
    })
    st.area_chart(time_data.set_index('Game'))

    progress_bar.progress(100)

    # Map with Points (Team's home location)
    st.header('Team Location')
    team_info = next(team for team in teams if team['id'] == team_id)
    lat = team_info.get('arena', {}).get('latitude')
    lon = team_info.get('arena', {}).get('longitude')
    if lat and lon:
        location_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(location_df)
    else:
        st.error('Location data not available for this team.')
else:
    st.error('No player data available.')

