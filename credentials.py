import os

sender = os.getenv('EMAIL_SENDER')
sender_app_password  = os.getenv('EMAIL_SENDER_APP_PASSWORD')

jwt_secret_key = os.getenv('JWT_SECRET_KEY')