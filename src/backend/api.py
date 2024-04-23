from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
import uvicorn
import pickle
from pydantic import BaseModel


class FeaturesModel(BaseModel):
    Venue: str
    Result: str
    GF: float
    GA: float
    Opponent: str
    xG: float
    xGA: float
    Team: str

app = FastAPI()


API_KEY= "PremierModel-2024$*"
API_KEY_NAME= "api_key"

api_key_query = APIKeyQuery(name =API_KEY_NAME, auto_error=False)

def get_api_key(api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.on_event("startup")
def load_model():

    global logged_model
    import mlflow
    mlflow.set_tracking_uri('https://dagshub.com/SantiagoAguirre2002/churn-app-2024-1.mlflow')
    logged_model = 'runs:/564ea0ecbc7b4a428244b2f27a2f61b0/logistic_classifier'

    # Load model as a PyFuncModel.
    logged_model = mlflow.pyfunc.load_model(logged_model)

@app.get("/api/v1/classify")
def classify(features_model: FeaturesModel, api_key : APIKey=Depends(get_api_key)):

    features= [val for val in features_model.__dict__.values()]
    prediction = logged_model.predict([features])


    label_dict= {
        0: "Draw",
        1: "Win",
        2: "Lose"
    }

    return {'prediction': label_dict[int(prediction[0])]}


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=5050, log_level='info', reload=True)





