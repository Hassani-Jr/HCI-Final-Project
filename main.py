import streamlit as st
import requests
import pandas as pd
import os
from datetime import date
import numpy as np
from dotenv import load_dotenv

load_dotenv()

headers = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

# Helper functions to fetch data
def fetch_teams():
    url = "https://api-nba-v1.p.rapidapi.com/teams"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'response' in data:
        return data['response']
    else:
        st.error("Error fetching teams data.")
        return []

def fetch_games(season, team_id):
    url = f"https://api-nba-v1.p.rapidapi.com/games?season={season}&team={team_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'response' in data:
        return data['response']
    else:
        st.error("Error fetching games data.")
        return []

def fetch_players(search_query=None, team_id=None, season=None):
    url = "https://api-nba-v1.p.rapidapi.com/players"
    params = {}
    if search_query:
        params['search'] = search_query
    if team_id:
        params['team'] = team_id
    if season:
        params['season'] = season
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if 'response' in data:
        return data['response']
    else:
        st.error("Error fetching players data.")
        return []

def fetch_player_stats(player_id, season):
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
    params = {
        'id': player_id,
        'season': season
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if 'response' in data:
        return data['response']
    else:
        st.error("Error fetching player statistics.")
        return []

def fetch_standings(season):
    url = f"https://api-nba-v1.p.rapidapi.com/standings?season={season}&league=standard"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'response' in data:
        return data['response']
    else:
        st.error("Error fetching standings data.")
        return []

# Title and Description
st.title('NBA Data Explorer')
st.write('Explore NBA teams, games, and player statistics using the API-NBA API.')
st.image('https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg', caption='NBA Logo')

# Dropdown for navigation
selection = st.selectbox("Select a section to explore:", ["Team Statistics", "Player Statistics", "Yearly Standings", "Player Search"])

# Fetch Teams Data
with st.spinner('Loading teams data...'):
    teams = fetch_teams()

# Progress Bar (Optional)
progress_bar = st.progress(0)
progress_bar.progress(20)

if selection == "Team Statistics":
    st.header('Team Statistics')
    # Interactive Dataframe
    if st.checkbox('Show Teams Data'):
        teams_df = pd.DataFrame(teams)
        st.dataframe(teams_df)
        st.success('Teams data loaded successfully!')

    progress_bar.progress(40)

    # Selectbox Widget
    st.subheader('Team Selection')
    team_names = [team['name'] for team in teams if team['nbaFranchise'] == True]
    selected_team = st.selectbox('Select a team:', team_names)

    # Get selected team ID
    team_id = next(team['id'] for team in teams if team['name'] == selected_team)

    # Date Input Widget
    selected_date = st.date_input('Select a date', date.today())

    # Button Widget
    if st.button('Fetch Games'):
        with st.spinner('Fetching games...'):
            games = fetch_games(season=2023, team_id=team_id)
            progress_bar.progress(60)
            games_on_date = [game for game in games if game['date']['start'].startswith(selected_date.strftime('%Y-%m-%d'))]
            if games_on_date:
                games_df = pd.DataFrame(games_on_date)
                st.dataframe(games_df)
                st.success(f"Found {len(games_on_date)} games on {selected_date.strftime('%Y-%m-%d')}.")
            else:
                st.warning(f"No games found on {selected_date.strftime('%Y-%m-%d')}.")
        progress_bar.progress(80)

    # Map with Points (Team's home location)
    st.subheader('Team Location')
    team_info = next(team for team in teams if team['id'] == team_id)
    lat = team_info.get('arena', {}).get('latitude')
    lon = team_info.get('arena', {}).get('longitude')
    if lat and lon:
        location_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(location_df)
    else:
        st.error('Location data not available for this team.')

    progress_bar.progress(100)

elif selection == "Player Statistics":
    st.header('Player Statistics')
    # Select Team
    team_names = [team['name'] for team in teams if team['nbaFranchise'] == True]
    selected_team = st.selectbox('Select a team:', team_names)

    # Get selected team ID
    team_id = next(team['id'] for team in teams if team['name'] == selected_team)

    # Slider Widget
    num_players = st.slider('Select number of players to display', 1, 15, 5)

    # Radio Button Widget
    stat_choice = st.radio('Select statistic to display:', ('Points', 'Rebounds', 'Assists'))

    # Fetch Players Data
    with st.spinner('Fetching players data...'):
        players = fetch_players(team_id=team_id, season=2023)
        progress_bar.progress(60)

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
    else:
        st.error('No player data available.')

elif selection == "Yearly Standings":
    st.header('Yearly Standings')
    # Fetch available seasons
    seasons_url = "https://api-nba-v1.p.rapidapi.com/seasons"
    seasons_response = requests.get(seasons_url, headers=headers)
    seasons_data = seasons_response.json()
    if 'response' in seasons_data:
        available_seasons = seasons_data['response']
    else:
        available_seasons = [str(year) for year in range(2023, 2000, -1)]
        st.warning("Could not fetch available seasons. Using default range.")

    # Select Season
    season = st.selectbox('Select a season:', sorted(available_seasons, reverse=True))
    if st.button('Fetch Standings'):
        with st.spinner('Fetching standings data...'):
            standings = fetch_standings(season=season)
            progress_bar.progress(60)

        standings_df = pd.DataFrame(standings)
        if not standings_df.empty:
            st.dataframe(standings_df)
            st.success(f"Standings for the {season} season loaded successfully!")
            progress_bar.progress(100)
        else:
            st.error('No standings data available.')

elif selection == "Player Search":
    st.header('Player Search')
    # Text Input for Player Name
    player_name = st.text_input('Enter player name to search:')
    if player_name:
        with st.spinner('Searching for players...'):
            search_results = fetch_players(search_query=player_name)
            progress_bar.progress(50)

        if search_results:
            # Create a DataFrame of search results
            search_df = pd.DataFrame(search_results)
            # Handle cases where multiple players are found
            st.subheader('Search Results')
            player_options = search_df['firstname'] + ' ' + search_df['lastname'] + ' (ID: ' + search_df['id'].astype(str) + ')'
            selected_player = st.selectbox('Select a player:', player_options)
            selected_player_id = int(selected_player.split('ID: ')[1].replace(')', ''))

            # Fetch available seasons
            seasons_url = "https://api-nba-v1.p.rapidapi.com/seasons"
            seasons_response = requests.get(seasons_url, headers=headers)
            seasons_data = seasons_response.json()
            if 'response' in seasons_data:
                available_seasons = seasons_data['response']
            else:
                available_seasons = [str(year) for year in range(2023, 2000, -1)]
                st.warning("Could not fetch available seasons. Using default range.")

            # Select Season
            season = st.selectbox('Select a season:', sorted(available_seasons, reverse=True))

            if st.button('Fetch Player Statistics'):
                with st.spinner('Fetching player statistics...'):
                    player_stats = fetch_player_stats(player_id=selected_player_id, season=season)
                    progress_bar.progress(80)

                if player_stats:
                    stats_df = pd.DataFrame(player_stats)
                    # Display statistics
                    st.subheader(f'Statistics for {selected_player} in {season}')
                    st.dataframe(stats_df)
                    progress_bar.progress(100)
                else:
                    st.error('No statistics available for this player in the selected season.')
        else:
            st.error('No players found with that name.')