from domain.entities.project.models import Project
from domain.services.entity_service import EntityService


class ProjectServiceInterface(EntityService[Project]): ...
