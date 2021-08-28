import environs

ENV = environs.Env()
ENV.read_env(".env")

# SECRET CONFIGURATION
SECRET_KEY = ENV("SECRET_KEY", default="")

# DEBUG CONFIGURATION
DEBUG = ENV("DEBUG", default=False)

# CACHE CONFIGURATION
CACHE_TYPE = ENV("CACHE_TYPE", default="simple")

# JWT CONFIGURATION
JWT_ALGORITHM = "RS256"
JWT_ALLOWED_ALGORITHMS = ["RS256"]
JWT_PRIVATE_KEY = ENV("PRIVATE_KEY", default="")
JWT_PUBLIC_KEY = ENV("PUBLIC_KEY", default="")

JWT_ACCESS_LIFESPAN = {"minutes": 15}

# Should be greater then JWT access lifespan
JWT_REFRESH_LIFESPAN = {"days": 30}
