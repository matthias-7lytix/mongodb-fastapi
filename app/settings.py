from dynaconf import Dynaconf
import os
settings = Dynaconf(settings_files=['settings.toml', '.secrets.toml'],
                    envvar_prefix="APP")
os.getenv("APP_MONGODB_USER")