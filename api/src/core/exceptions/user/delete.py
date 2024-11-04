class UserIsAdminOfOrgsException(Exception):
    """
    Кастомное исключение для случая, когда пользователь является администратором организации.
    """

    def __init__(self, orgs):
        self.orgs = orgs
        super().__init__(f"User is admin of orgs: {' '.join(map(str, orgs))}")
