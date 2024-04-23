import streamlit as st
import pandas as pd
import requests
import json

st.markdown("""
# Gameday Premier League Prediction

Enter customer details to predict result
""")

st.sidebar.header("Gameday Details:")
Venue = st.sidebar.number_input("Venue (0 or 1)", min_value=0.0, max_value=1.0, value=0.0)
Opponent = st.sidebar.number_input("Opponent", min_value=0.0, value=19.0)
xG = st.sidebar.number_input("xG" , min_value=0.0, value=5.0)
xGA = st.sidebar.number_input("xGA", min_value=0.0, value=5.0)
Referee = st.sidebar.number_input("Referee", min_value=0.0, value=24.0)
Team = st.sidebar.number_input("Team", min_value=0.0, value=19.0)
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
    st.write("Prediction: ",response.json())

    print(response.text)