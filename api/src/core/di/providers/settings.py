from dishka import Provider, Scope, provide
from config import JWTSettings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP, provides=JWTSettings)
    def provide_auth_settings(self) -> JWTSettings:
        return JWTSettings()
