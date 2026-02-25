import torch
import torch.nn as nn
from torchvision import models
from typing import Literal


_models = {}

# -----------------------------
# Build architectures
# -----------------------------
def _build_transfer_model(num_classes=6):
    model = models.mobilenet_v2(weights=None)
    model.classifier = nn.Sequential(
        nn.Linear(model.last_channel, 128),
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(128, 6)
    )
    return model


def _build_scratch_model(num_classes=6):
    # ⚠️ Replace this with your real CustomCNN if different
    from src.models.custom_cnn import CustomCNN
    return CustomCNN(num_classes=num_classes)


# -----------------------------
# Fixed loader
# -----------------------------
def _load_model(path, device, model_type: Literal["t", "s"]):
    state_dict = torch.load(path, map_location=device)

    # Build correct architecture
    if model_type == "t":
        model = _build_transfer_model()
    else:
        model = _build_scratch_model()

    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


# -----------------------------
# Public API (unchanged)
# -----------------------------
def get_model(cfg, model: Literal["t", "s"], device=None):
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    if model not in _models:
        if model == "t":
            _models[model] = _load_model(
                cfg["MODEL_TRANSFER_PATH"], device, "t"
            )
        elif model == "s":
            _models[model] = _load_model(
                cfg["MODEL_SCRATCH_PATH"], device, "s"
            )
        else:
            raise ValueError("model must be 't' or 's'")

    return _models[model]