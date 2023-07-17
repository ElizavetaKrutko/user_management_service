from functools import lru_cache

from app.common import app_settings

environments = {
    app_settings.EnvironmentTypes.dev: app_settings.DevelopmentSettings,
    app_settings.EnvironmentTypes.test: app_settings.TestSettings,
    app_settings.EnvironmentTypes.prod: app_settings.ProductionSettings,
    app_settings.EnvironmentTypes.local: app_settings.LocalSettings,
}


@lru_cache
def get_settings() -> app_settings.BaseAppSettings:
    app_env = app_settings.BaseAppSettings().environment
    return environments[app_env]()


settings = get_settings()
