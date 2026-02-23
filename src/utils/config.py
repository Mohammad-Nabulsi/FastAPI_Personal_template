import dotenv
import os

def load_config(envfile: str = '.env') -> dict:
    """
    Load configuration from a .env file and return it as a dictionary.

    Args:
        envfile (str): Path to the .env file. Defaults to '.env'.
    Returns:
        dict: A dictionary containing the configuration key-value pairs.
    """
    dotenv.load_dotenv(envfile, override=True)
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    artifact_dir = os.path.join(SRC_DIR, './artifacts')
    ARTIFACT_DIR = os.path.normpath(artifact_dir)
    APP_NAME = os.getenv('APP_NAME', 'default_app')
    VERSION = os.getenv('VERSION', '1.0.0')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    MODEL_PATH = os.path.join(ARTIFACT_DIR, 'model.pt')

    config = {
        'APP_NAME': APP_NAME,
        'VERSION': VERSION,
        'SECRET_KEY': SECRET_KEY,
        'MODEL_PATH': MODEL_PATH,
    }

    return config
# Example usage

if __name__ == "__main__":
    config = load_config()
    print(config)