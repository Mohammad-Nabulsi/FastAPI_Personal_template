from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from src.utils.config import load_config

# example
from src.schemas.response import predictionResponse
from src.inference import classify_image
cfg = load_config()

app = FastAPI(title=cfg['APP_NAME'], version=cfg['VERSION'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name='X-API-Key')
async def verify_api_key(api_key: str=Depends(api_key_header)):
    if api_key != cfg['SECRET_KEY']:
        raise HTTPException(status_code=403, detail="You are not authorized to use this API")
    return api_key


@app.get('/', tags=['check'])
async def home(api_key: str=Depends(verify_api_key)):
    return {
        "message": "up & running"
    }

@app.post("/classify", tags=['NN'], response_model=predictionResponse)
async def classify(file: UploadFile, api_key: str=Depends(verify_api_key)):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "File must be an image")
            
        contents = await file.read()
        response = classify_image(contents)
        return predictionResponse(**response)
    
    except Exception as e:
        raise HTTPException(500, f"Error making predictions: {str(e)}")