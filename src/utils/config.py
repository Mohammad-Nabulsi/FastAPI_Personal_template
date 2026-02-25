import dotenv
import os
import joblib

def load_config(envfile: str = '.env') -> dict:
    """
    Load configuration from a .env file and return it as a dictionary.

    Args:
        envfile (str): Path to the .env file. Defaults to '.env'.
    Returns:
        dict: A dictionary containing the configuration key-value pairs.
    """

# ======= LOADING
    dotenv.load_dotenv(envfile, override=True)

# ======== ROOT PATH
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    artifact_dir = os.path.join(SRC_DIR, './assets')
    ARTIFACT_DIR = os.path.normpath(artifact_dir)

# ======== PATH JOINING
    MODEL_SCRATCH_PATH = os.path.join(ARTIFACT_DIR, 'intel-scratch.pt')
    MODEL_TRANSFER_PATH = os.path.join(ARTIFACT_DIR, 'intel-mobilenet.pt')
    IDXMAPPING_PATH = os.path.join(ARTIFACT_DIR, 'idx2label.joblib')
    IDX2LABEL = joblib.load(IDXMAPPING_PATH)
# ======== VERSIONING
    APP_NAME = os.getenv('APP_NAME', 'default_app')
    VERSION = os.getenv('VERSION', '1.0.0')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')

# ======== RETURNED CONFIGURATIONS
    config = {
        'APP_NAME': APP_NAME,
        'VERSION': VERSION,
        'SECRET_KEY': SECRET_KEY,
        'MODEL_SCRATCH_PATH': MODEL_SCRATCH_PATH,
        'MODEL_TRANSFER_PATH': MODEL_TRANSFER_PATH,
        'IDX2LABEL': IDX2LABEL,
    }

    return config
# Example usage

if __name__ == "__main__":
    config = load_config()
    print(config)