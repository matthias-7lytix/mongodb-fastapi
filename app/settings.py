from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml', '.secrets.toml'],
                    envvar_prefix="APP")