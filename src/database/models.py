import datetime
import peewee
import redis

from src.config.config import SETTINGS

if SETTINGS.DB_ENGINE == 'sqlite3':
    db = peewee.SqliteDatabase(SETTINGS.DB_NAME)
elif SETTINGS.DB_ENGINE == 'mysql':
    db = peewee.MySQLDatabase(
        SETTINGS.DB_NAME,
        user=SETTINGS.DB_USER,
        password=SETTINGS.DB_PASSWORD,
        host=SETTINGS.DB_HOST,
        port=SETTINGS.DB_PORT
    )
else:
    raise ValueError("Unsupported database engine. Please use 'sqlite3' or 'mysql'.")

if SETTINGS.ACTIVE_REDIS:
    redis_db = redis.Redis(host=SETTINGS.DB_HOST, port=6379, db=0, encoding='utf-8')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = peewee.BigIntegerField(unique=True)
    step = peewee.CharField(max_length=255, default='none') # Default 'none' step
    language = peewee.CharField(max_length=5, default='en') # Default 'English' Language
    account_status = peewee.BooleanField(default=True) # True: Free / False: Blocked
    datetime_subscription = peewee.DateTimeField(default=lambda: datetime.datetime.now() + datetime.timedelta(days=1)) # default 1 day subscription
    datetime_joined = peewee.DateTimeField(default=datetime.datetime.now) # Added auto (now)


db.connect()
db.create_tables([User])
