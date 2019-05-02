import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a2BxpjeRLJBOyTWluc0NqA'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="AdhanRazzaque",
        password="wT29UKmRESNuGPt",
        hostname="AdhanRazzaque.mysql.pythonanywhere-services.com",
        databasename="AdhanRazzaque$projectmgmtdb",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 280

