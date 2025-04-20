"""Configurar una aplicación Flask."""


class Config:
    """Configuración de la aplicación Flask."""

    # DEBO ARREGLAR ESTO PORQUE PARECE QUE NO FUNCIONA CON EL IPADDRESS O LE VALE

    DEBUG = True
    TESTING = True

    # Database configuration
    DATABASE_USER = "root"
    DATABASE_PASSWORD = "1234"
    IP_ADDRESS = "localhost"
    PORT = 3306
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{IP_ADDRESS}:{PORT}/tlacuachin"
    SESSION_COOKIE_SAMESITE = 'Lax'
    SECRET_KEY = '$up3r_$3cr31_43y'
    UPLOAD_FOLDER = './src/static/img/'

    # Track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Configuración extendida para producción."""

    DEBUG = False
    TESTING = False


class DeveloperConfig(Config):
    """Configuración extendida para desarrollar."""

    DEBUG = True
    SECRET_KEY = 'dev'
    TESTING = True
