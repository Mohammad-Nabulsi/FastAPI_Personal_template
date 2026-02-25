from fastapi import FastAPI, HTTPException, Depends, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from src.utils.config import load_config
from typing import Literal
from src.models.schema import PredictionResponse
from src.inference import ImageClassifier

cfg = load_config()

app = FastAPI(title=cfg['APP_NAME'], version=cfg['VERSION'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API KEY SECURITY
# -----------------------------
api_key_header = APIKeyHeader(name='X-API-Key')

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != cfg['SECRET_KEY']:
        raise HTTPException(status_code=403, detail="You are not authorized")
    return api_key


# -----------------------------
# LOAD CLASSIFIER ON STARTUP
# -----------------------------
classifier_t = ImageClassifier(model_type="t")
classifier_s = ImageClassifier(model_type="s")


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get('/', tags=['check'])
async def home(api_key: str = Depends(verify_api_key)):
    return {"message": "up & running"}


# -----------------------------
# SINGLE IMAGE CLASSIFICATION
# -----------------------------
@app.post("/classify", tags=['NN'], response_model=PredictionResponse)
async def classify(
    file: UploadFile,
    model: Literal["t", "s"] = "t",
    api_key: str = Depends(verify_api_key),
):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "File must be an image")

        contents = await file.read()

        # select model
        classifier = classifier_t if model == "t" else classifier_s

        result = classifier.predict_batch([contents]).predictions[0]
        return result

    except Exception as e:
        raise HTTPException(500, f"Error making predictions: {str(e)}")