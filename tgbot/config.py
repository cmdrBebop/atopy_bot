from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    mindbox_secret_key: str


@dataclass
class GoogleSheets:
    credentials_file: str
    spreadsheet_id: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    google_sheets: GoogleSheets


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            mindbox_secret_key=env.str('MINDBOX_SECRET_KEY')
        ),
        google_sheets=GoogleSheets(
            spreadsheet_id=env.str('SPREADSHEET_ID'),
            credentials_file=env.str('CREDENTIALS_FILE')
        )
    )
