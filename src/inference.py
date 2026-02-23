from .utils.config import load_config
from .utils.model_registry import get_model
from .schemas.response import predictionResponse
import torch
import numpy as np


cfg = load_config()
model = get_model(cfg)

# Your function below