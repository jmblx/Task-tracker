# from core.exceptions.tasks.valdiation import InvalidTaskData


class CreateTaskValidator:
    def validate_create_data(self, task: dict) -> None:
        self._validate_bound(task)
