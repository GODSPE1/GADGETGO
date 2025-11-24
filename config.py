import os

class Config:
    """configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'
    # Add other production configs here if needed