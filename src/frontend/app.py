import streamlit as st
import pandas as pd
import requests
import json

# Estilo de la barra lateral
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(to right top, #051937, #004d7a, #008793, #00bf72, #a8eb12);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Estilo del encabezado
st.markdown("""
<style>
h1 {
    color: #004d7a;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Estilo del cuerpo principal
st.markdown("""
<style>
.reportview-container {
    background-color: #ffffff;
    color: #004d7a;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# Gameday Premier League Predictions
""")


#lista de quipos
team_list = [

    "Liverpool",
    "Manchester City",
    "Newcastle Utd",
    "Burnley",
    "Wolves",
    "Arsenal",
    "Manchester Utd",
    "Brighton",
    "Everton",
    "Crystal Palace",
    "Sheffield Utd",
    "Fulham",
    "Chelsea",
    "Brentford",
    "Bournemouth",
    "Nott'ham Forest",
    "Tottenham",
    "West Ham",
    "Aston Villa",
    "Luton Town"
]
team_list_2 = [
    "Liverpool",
    "NewcastleUnited",
    "Burnley",
    "Everton",
    "CrystalPalace",
    "Fulham",
    "ManchesterCity",
    "SheffieldUnited",
    "WolverhamptonWanderers",
    "BrightonandHoveAlbion",
    "ManchesterUnited",
    "Arsenal",
    "WestHamUnited",
    "TottenhamHotspur",
    "Bournemouth",
    "Brentford",
    "NottinghamForest",
    "AstonVilla",
    "LutonTown",
    "Chelsea"
]
referee_list = [
    "Anthony Taylor",
    "Michael Oliver",
    "Paul Tierney",
    "Andy Madley",
    "Tim Robinson",
    "John Brooks",
    "Simon Hooper",
    "Robert Jones",
    "Chris Kavanagh",
    "Jarred Gillett",
    "Craig Pawson",
    "Stuart Attwell",
    "Samuel Barrott",
    "David Coote",
    "Michael Salisbury",
    "Peter Bankes",
    "Thomas Bramall",
    "Darren England",
    "Joshua Smith",
    "Tony Harrington",
    "Darren Bond",
    "Lewis Smith",
    "Graham Scott",
    "Rebecca Welch",
    "Robert Madley",
    "Samuel Allison"
]

# Valores únicos y ordenados para xG y xGA
xG_values = [1.1, 1.3, 1.2, 1.4, 0.7, 0.9, 2.2, 0.6, 1.5, 1.8, 1.7, 0.8, 0.5, 1.6, 2.3, 2.4, 0.3, 1.9, 2.1, 0.4, 2.9,
             2.6, 2.5, 2.8, 3.0, 2.0, 3.3, 3.1, 3.5, 3.2, 0.2, 4.0, 2.7, 3.6, 4.1, 0.1, 3.4, 3.8, 7.0, 3.9, 3.7, 0.0]
xGA_values = [1.1, 1.3, 1.4, 1.2, 0.7, 0.6, 2.2, 0.9, 1.5, 1.8, 1.7, 0.5, 0.8, 1.6, 2.3, 0.3, 2.4, 1.9, 2.1, 0.4, 2.9,
              2.5, 2.6, 2.8, 3.0, 2.0, 3.3, 3.1, 3.2, 3.5, 0.2, 4.1, 4.0, 0.1, 2.7, 3.6, 3.4, 3.7, 0.0, 7.0, 3.8, 3.9]

# Eliminar duplicados y ordenar valores
unique_xG_values = sorted(set(xG_values))
unique_xGA_values = sorted(set(xGA_values))

st.sidebar.header("Gameday Details:")
Venue = st.sidebar.selectbox("Venue", ["Home", "Away"])
Opponent = st.sidebar.selectbox("Opponent", team_list)
xG = st.sidebar.selectbox("xG (Expected goals)", options=unique_xG_values, format_func=lambda x: f"{x:.1f}")
xGA = st.sidebar.selectbox("xGA (Expected goals against)", options=unique_xGA_values, format_func=lambda x: f"{x:.1f}")
Referee = st.sidebar.selectbox("Referee", referee_list)
Team = st.sidebar.selectbox("Team", team_list_2)
# Add other parameters as needed

dict_input = {
    "Venue" : Venue,
    "Opponent" : Opponent,
    "xG": xG,
    "xGA": xGA,
    "Referee": Referee,
    "Team": Team
}

df_input = pd.DataFrame(dict_input, index=[0])
st.subheader("Gameday Predict")

st.write(df_input)


if st.button("predict"):
    url = "http://api-result:5050/api/v1/classify?api_key=PremierModel-2024$*"
    payload = json.dumps(dict_input)

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    st.write("Prediction: ",response.json()['prediction'])

    print(response.text)

#