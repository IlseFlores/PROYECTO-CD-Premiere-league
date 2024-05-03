from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import uvicorn
import pickle
from pydantic import BaseModel


class FeaturesModel(BaseModel):
    Venue: str
    Opponent: str
    xG: float
    xGA: float
    Referee: str
    Team: str


app = FastAPI()

API_KEY = "PremierModel-2024$*"
API_KEY_NAME = "api_key"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.on_event("startup")
def load_model():
    global logged_model, x_encoder
    import mlflow
    mlflow.set_tracking_uri('https://dagshub.com/IlseFlores/PROYECTO-CD-Premiere-league.mlflow')
    logged_model = 'runs:/0649f75408284b19862142283f8a69b9/logistic_regression_classifier'

    # Load model as a PyFuncModel
    logged_model = mlflow.pyfunc.load_model(logged_model)

    # Load x_encoder from pickle file
    with open("x_encode.pkl", "rb") as file:
        x_encoder = pickle.load(file)


@app.get("/api/v1/classify")
def classify(features_model: FeaturesModel, api_key: APIKey = Depends(get_api_key)):
    global logged_model, x_encoder

    # Convert FeaturesModel to a list of feature values
    features = [val for val in features_model.__dict__.values()]

    # Transform features using x_encoder
    features_transformed = x_encoder.transform([features])

    # Predict using loaded model
    prediction = logged_model.predict(features_transformed)

    label_dict = {0: "Draw", 1: "Win", 2: "Lose"}

    return {'prediction': label_dict[int(prediction[0])]}


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=5050, log_level='info', reload=True)
