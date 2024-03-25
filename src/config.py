class Config:
    SECRET_KEY = "B!1poNAt1T^%kvhUI*S^"


class DevelopmentConfig(Config):
    MYSQL_HOST = "192.168.0.109"
    MYSQL_USER = "tecnico"
    MYSQL_PASSWORD = "admin-tecnico"
    MYSQL_DB = "SIG_CENTER"
    MYSQL_PORT = 3307


config = {"development": DevelopmentConfig}
