from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import uvicorn
import pickle
import mlflow
from pydantic import BaseModel


class FeaturesModel(BaseModel):
    Venue: str
    Referee: str
    Opponent: str
    xG: float
    xGA: float
    Team: str


app = FastAPI()

# Configuración de la clave API
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
    global logged_model, encode
    try:
        mlflow.set_tracking_uri('https://dagshub.com/IlseFlores/PROYECTO-CD-Premiere-league.mlflow')
        logged_model_path = 'runs:/0649f75408284b19862142283f8a69b9/logistic_regression_classifier'
        logged_model = mlflow.pyfunc.load_model(logged_model_path)
        print("Model loaded successfully")

        # Load encoder
        encoder_path = 'x_encode.pkl'
        with open(encoder_path, 'rb') as f:
            encode = pickle.load(f)
        print("Encoder loaded successfully")

    except Exception as e:
        print("Error loading model or encoder:", str(e))
        raise


@app.get("/api/v1/classify")
def classify(features_model: FeaturesModel, api_key: APIKey = Depends(get_api_key)):
    global logged_model, encode
    try:
        complaint_tokenized = encode.transform([[features_model.Venue, features_model.Referee, features_model.Opponent,
                                                 features_model.xG, features_model.xGA, features_model.Team]])
        prediction = logged_model.predict(complaint_tokenized)

        label_dict = {
            0: "Draw",
            1: "Win",
            2: "Lose"
        }
        return {'prediction': label_dict[int(prediction[0])]}
    except Exception as e:
        print("Error processing request:", str(e))
        raise HTTPException(status_code=500, detail="Error processing request")


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=5050, log_level='info', reload=True)
