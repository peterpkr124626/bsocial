from .config import settings

DATABASE_PROVIDER = settings.database_provider
DATABASE_NAME = settings.database_name
DATABASE_USERNAME = settings.database_username
DATABASE_PASSWORD = settings.database_password
DATABASE_HOSTNAME = settings.database_hostname
SQLALCHEMY_DATABASE_URL = f"{DATABASE_PROVIDER}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}"
