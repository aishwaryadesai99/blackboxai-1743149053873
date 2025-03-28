import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-123'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'jwt-dev-secret-456'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///payroll.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Payroll Settings
    OVERTIME_RATE = float(os.getenv('OVERTIME_RATE') or 1.5)  # Time-and-a-half for overtime
    HOLIDAY_RATE = float(os.getenv('HOLIDAY_RATE') or 2.0)    # Double time for holidays
    TAX_RATE = float(os.getenv('TAX_RATE') or 0.15)           # Default tax rate
    NIGHT_SHIFT_PREMIUM = float(os.getenv('NIGHT_SHIFT_PREMIUM') or 0.2)  # 20% extra
    
    # Application Settings
    ENV = os.getenv('FLASK_ENV') or 'development'
    DEBUG = os.getenv('FLASK_DEBUG') == '1'
    
    # File Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER') or 'uploads'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS') or '*'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL') or 'INFO'
