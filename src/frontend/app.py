import streamlit as st
import pandas as pd
import requests
import json


st.markdown("""
# Gameday Premier League Predictions

Enter customer details to predict result
""")

st.sidebar.header("Gameday Details:")
Venue = st.sidebar.selectbox("Venue (0 or 1)", ("0", "1"))
Opponent = st.sidebar.selectbox("Opponent", ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16", "17", "18","19"))
xG = st.sidebar.number_input("xG" , min_value=0.0, max_value=7.0, step=0.1)
xGA = st.sidebar.number_input("xGA", min_value=0.0, max_value=7.0, step=0.1)
Referee = st.sidebar.selectbox("Referee", ("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16", "17", "18","19","20","21","22","23","24","25"))
Team = st.sidebar.selectbox("Team",("0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16", "17", "18","19"))
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
    st.write("Prediction: ",response.json()["prediction"])

    print(response.text)

