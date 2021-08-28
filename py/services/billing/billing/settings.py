import environs

ENV = environs.Env()
ENV.read_env(".env")

# SECRET CONFIGURATION
SECRET_KEY = ENV("SECRET_KEY", default="")

# DEBUG CONFIGURATION
DEBUG = ENV("DEBUG", default=False)

# SQLALCHEMY CONFIGURATION
DB_HOST = ENV("DB_HOST", default="")
DB_NAME = ENV("DB_NAME", default="")
DB_USER = ENV("DB_USER", default="")
DB_PASSWORD = ENV("DB_PASSWORD", default="")

SQLALCHEMY_DATABASE_URI = ENV(
    "SQLALCHEMY_DATABASE_URI", default=f"postgresql://{DB_NAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_MODEL_IMPORTS = ("billing.models.account", "billing.models.balance_transaction")
