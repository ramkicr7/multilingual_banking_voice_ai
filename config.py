import os

class Config:

    SECRET_KEY = "  9f4c2a8d3b7e5f1a6c8d0e2b4a9f6c3d8e1a2b5c7d9f0a1b2c3d4e5f6a7b8c9"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "rmbi.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # EMAIL CONFIG
    MAIL_EMAIL = "ramkishoreelumalai@gmail.com"
    MAIL_PASSWORD = "klop exmi eovx zoyi"
   