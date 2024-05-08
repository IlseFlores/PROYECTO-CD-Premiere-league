import streamlit as st
import pandas as pd
import requests
import json

st.markdown("""
# Gameday Premier League Predictions

Enter customer details to predict result
""")

#lista de quipos
team_list = [
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


st.sidebar.header("Gameday Details:")
Venue = st.sidebar.selectbox("Venue", ["Home", "Away"])
Opponent = st.sidebar.selectbox("Opponent", team_list)
xG = st.sidebar.number_input("xG" , min_value=0.0, value=5.0)
xGA = st.sidebar.number_input("xGA", min_value=0.0, value=5.0)
Referee = st.sidebar.selectbox("Referee", referee_list)
Team = st.sidebar.selectbox("Team", team_list)
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