import streamlit as st
import requests
import pandas as pd

st.title("Pokémon Explorer")

# Functions
@st.cache_data
def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@st.cache_data
def get_pokemon_species_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
@st.cache_data
def get_pokemon_location_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/encounters"
    response = requests.get(url)
    if response.status_code == 200:
        locations = response.json()
        if locations:
            location_data = [{"lat": loc["location_area"]["name"], "lon": 0} for loc in locations]
            return pd.DataFrame(location_data)
    return None

@st.cache_data
def fetch_evolution_chain(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/")
    if response.status_code == 200:
        species_data = response.json()
        evolution_chain_url = species_data["evolution_chain"]["url"]
        evolution_response = requests.get(evolution_chain_url)
        if evolution_response.status_code == 200:
            return evolution_response.json()
    return None


# Function to fetch Pokémon location data
def fetch_pokemon_locations(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/encounters"
    response = requests.get(url)
    if response.status_code == 200:
        locations = response.json()
        location_data = []

        for loc in locations:
            location_area = loc["location_area"]["name"]
            lat = hash(location_area) % 90
            lon = hash(location_area) % 180
            location_data.append({"lat": lat, "lon": lon, "location_area": location_area})

        return pd.DataFrame(location_data)
    return pd.DataFrame(columns=["lat", "lon", "location_area"])

@st.cache_data
# Function to extract all evolutions from the chain
def get_evolution_chain(evolution_data):
    chain = []
    current = evolution_data["chain"]

    while current:
        chain.append(current["species"]["name"])
        if current["evolves_to"]:
            # Move to the next evolution
            current = current["evolves_to"][0]
        else:
            # End of the chain
            current = None

    return chain

@st.cache_data
def fetch_stats_for_chain(pokemon_chain):
    stats = []
    for pokemon in pokemon_chain:
        data = get_pokemon_data(pokemon)
        if data:
            stat_data = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
            stat_data["name"] = data["name"]
            stats.append(stat_data)
    return pd.DataFrame(stats)

st.header("Search Pokémon")

# Use columns to organize input widgets
col1, col2 = st.columns(2)

with col1:
    search_method = st.selectbox(
    "Choose Search Method",
    ["Search by Name", "Search by ID"]
)
    
if search_method == "Search by Name":
    pokemon_name = st.text_input("Enter Pokémon Name", value="pikachu")
    st.write(f"Searching for Pokémon by Name: **{pokemon_name}**")
else:
    pokemon_id = st.number_input("Enter Pokémon ID", min_value=1, max_value=1010)
    pokemon_name = None
    st.write(f"Searching for Pokémon by ID: **{int(pokemon_id)}**")
    
fetch_data = st.button("Fetch Pokémon Data")

max_moves = st.number_input("Maximum Moves to Display", min_value=1, max_value=100, value=5)

stat_display_type = st.radio(
    "Select how to display stats:",
    options=["Bar Chart", "Line Chart"]
)

stat_focus = st.multiselect(
    "Select Stats to Focus On",
    ["hp", "attack", "defense", "special-attack", "special-defense", "speed"],
    default=["hp", "attack", "speed"]
)


# Main Application Logic
if fetch_data:
    if pokemon_name:
        data = get_pokemon_data(pokemon_name)
        species_data = get_pokemon_species_data(pokemon_name)
        pokemon_name = data['name'] if data else ""
    else:
        data = get_pokemon_data(str(int(pokemon_id)))
        species_data = get_pokemon_species_data(str(int(pokemon_id)))
        pokemon_name = data['name'] if data else ""
        pokemon_id = data['id'] if data else ""

    if data and species_data:

        st.success(f"Successfully fetched data for {pokemon_name.title()}!")

        image_url = data['sprites']['front_default']
        if image_url:
            st.image(image_url, caption=pokemon_name.title())

        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {pokemon_name.title()}")
            st.write(f"**ID:** {data['id']}")
            st.write(f"**Height:** {data['height']}")
            st.write(f"**Weight:** {data['weight']}")
        with col2:
            st.write(f"**Base Experience:** {data['base_experience']}")
            types = [t['type']['name'] for t in data['types']]
            st.write(f"**Types:** {', '.join(types)}")
            abilities = [a['ability']['name'] for a in data['abilities']]
            st.write(f"**Abilities:** {', '.join(abilities)}")

        st.subheader("Stats")
        stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        focused_stats = {k: stats[k] for k in stat_focus if k in stats}

        stats_df = pd.DataFrame(focused_stats.items(), columns=["Stat", "Value"]).set_index("Stat")

        if stat_display_type == "Bar Chart":
            st.bar_chart(stats_df)
        else:
            st.line_chart(stats_df)


        # Moves
        st.subheader("Moves")
        moves = [move["move"]["name"] for move in data["moves"][:max_moves]]
        st.write(f"Displaying up to {max_moves} moves:")
        moves_df = pd.DataFrame(moves, columns=['Moves'])
        st.dataframe(moves_df)
        
        
        evolution_data = fetch_evolution_chain(pokemon_name)
        if evolution_data:
            evolution_chain = get_evolution_chain(evolution_data)
            st.write(f"Evolution Chain: {' → '.join(evolution_chain).capitalize()}")
            stats_df = fetch_stats_for_chain(evolution_chain)
            st.subheader("Stat Progression Across Evolutions")
            st.line_chart(stats_df.set_index("name"))
        else:
            st.error("No evolution chain found for this Pokémon.")
            
        st.subheader("Pokémon Locations")
        locations_df = fetch_pokemon_locations(pokemon_name)
        if not locations_df.empty:
            st.map(locations_df[["lat", "lon"]])
            st.write("Locations:")
            st.table(locations_df)
        else:
            st.info("No location data available for this Pokémon.")
    else:
        st.error("Pokémon not found. Please check the name or ID and try again.")
else:
    st.info("Enter a Pokémon name or ID and click 'Fetch Pokémon Data' to begin.")
