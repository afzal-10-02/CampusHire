from datetime import timedelta


class LocalConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///campushire.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CORS_RESOURCES = {r"/*": {"origins": "*"}} 

    JWT_SECRET_KEY =  "78huh8@4@#$@Jfdis%^$Qm3tkgmbk#4%44tgtgfm46345$%$#%@##$%&@$$f"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)
    JWT_COOKIE_CSRF_PROTECT = False  


    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""


    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0 




class ProductionConfig:
    DEBUG = False