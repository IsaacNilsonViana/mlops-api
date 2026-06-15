import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from typing import List

modelo = joblib.load("modelo/wine_rf.joblib")

FEATURES = ["alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
            "total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins",
            "color_intensity", "hue", "od280/od315_of_diluted_wines", "proline"]

app = FastAPI()

class Entrada(BaseModel):
    features: List[float]

    @field_validator("features")
    def valida_13(cls, v):
        if len(v) != 13:
            raise ValueError("Exatamente 13 features")
        return v

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {
        "algoritmo": type(modelo).__name__,
        "classes": modelo.classes_.tolist(),
        "n_features": 13
    }

@app.post("/predict")
def predict(dados: Entrada):
    df = pd.DataFrame([dados.features], columns=FEATURES)
    return {
        "classe": int(modelo.predict(df)[0]),
        "probabilidades": modelo.predict_proba(df)[0].tolist()
    }
