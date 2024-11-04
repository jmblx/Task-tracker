from dishka import Provider, Scope, provide

from config import JWTSettings, MinIOConfig


class SettingsProvider(Provider):
    jwt_settings = provide(
        lambda *args: JWTSettings(), scope=Scope.APP, provides=JWTSettings
    )
    storage_settings = provide(
        lambda *args: MinIOConfig(), scope=Scope.APP, provides=MinIOConfig
    )
    # @provide(scope=Scope.APP, provides=JWTSettings)
    # def provide_auth_settings(self) -> JWTSettings:
    #     return JWTSettings()
