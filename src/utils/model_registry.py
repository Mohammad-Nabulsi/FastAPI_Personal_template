import torch

_model = None

def get_model(cfg, device=None):
    global _model
    if _model is None:
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        _model = torch.load(cfg["MODEL_PATH"], map_location=device)
        _model.eval()  

    return _model