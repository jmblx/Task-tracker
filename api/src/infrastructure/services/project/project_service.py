from domain.entities.project.models import Project
from domain.repositories.project.repo import ProjectRepository
from domain.services.project.project_service_interface import ProjectServiceInterface
from infrastructure.services.entity_service_impl import EntityServiceImpl


class ProjectServiceImpl(EntityServiceImpl[Project], ProjectServiceInterface):
    def __init__(self, base_repo: ProjectRepository):
        super().__init__(base_repo)
