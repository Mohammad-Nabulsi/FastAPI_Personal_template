import io
import os
from typing import List, Union

import numpy as np
from PIL import Image
import torch
from torchvision import transforms

from .utils.config import load_config
from .models.schema import PredictionResponse, PredictionsResponse
from .utils.model_registry import get_model

CFG = load_config()
IDX2LABEL = CFG['IDX2LABEL']

class ImageClassifier:
    def __init__(self, model_type: str = "t", target_size=(100, 100)):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = get_model(CFG, model_type, self.device)
        self.idx2label = IDX2LABEL
        self.target_size = target_size

        self.transform = transforms.Compose([
            transforms.Resize(target_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],   # MobileNet normalization
                std=[0.229, 0.224, 0.225]
            )
        ])

    # ----------------------------
    # Preprocess
    # ----------------------------
    def _preprocess_image(self, image_data: Union[str, bytes]) -> torch.Tensor:
        try:
            if isinstance(image_data, str):
                image = Image.open(image_data).convert("RGB")
            else:
                image = Image.open(io.BytesIO(image_data)).convert("RGB")

            tensor = self.transform(image)
            return tensor.unsqueeze(0)  # add batch dim

        except Exception as e:
            raise ValueError(f"Error preprocessing image: {str(e)}")

    # ----------------------------
    # Batch prediction
    # ----------------------------
    def predict_batch(self, images_data: List[Union[str, bytes]]) -> PredictionsResponse:
        if not images_data:
            raise ValueError("No images provided for prediction")

        basenames = []
        tensors = []

        for i, img_data in enumerate(images_data):
            if isinstance(img_data, str) and os.path.exists(img_data):
                basenames.append(os.path.basename(img_data))
            else:
                basenames.append(f"image_{i}")

            tensors.append(self._preprocess_image(img_data))

        batch = torch.cat(tensors).to(self.device)

        with torch.no_grad():
            logits = self.model(batch)
            probs = torch.softmax(logits, dim=1)

        predicted_class_indices = probs.argmax(dim=1).cpu().numpy()
        confidence_scores = (probs.max(dim=1).values * 100).cpu().numpy()

        predicted_class_names = [
            self.idx2label[int(idx)] for idx in predicted_class_indices
        ]

        prediction_responses = [
            PredictionResponse(
                base_name=basename,
                class_index=int(idx),
                class_name=name,
                confidence=round(float(score), 2),
            )
            for basename, idx, name, score in zip(
                basenames,
                predicted_class_indices,
                predicted_class_names,
                confidence_scores,
            )
        ]

        return PredictionsResponse(predictions=prediction_responses)