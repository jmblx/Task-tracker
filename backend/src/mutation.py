import strawberry
from uuid import UUID

from auth.models import User, Role
from organization.models import Organization
from project.models import Project
from task.models import Task, Group
from gql_types import UserCreateType, UserUpdateType, RoleCreateType, RoleUpdateType, OrganizationCreateType,\
    OrganizationUpdateType, ProjectCreateType, ProjectUpdateType, TaskCreateType, TaskUpdateType
from utils import insert_obj, update_object, insert_task, prepare_data_mailing, send_task_updates

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_role(self, data: RoleCreateType) -> int:
        obj_id = await insert_obj(Role, data.__dict__)
        return obj_id

    @strawberry.mutation
    async def update_role(self, item_id: int, data: RoleUpdateType) -> bool:
        await update_object(data.__dict__, Role, item_id)
        return True

    @strawberry.mutation
    async def update_user(self, id: UUID, data: UserUpdateType) -> bool:
        await update_object(data.__dict__, User, id)
        return True

    @strawberry.mutation
    async def add_organization(self, data: OrganizationCreateType) -> int:
        obj_id = await insert_obj(Organization, data.__dict__)
        return obj_id

    @strawberry.mutation
    async def update_organization(self, id: int, data: OrganizationUpdateType) -> bool:
        await update_object(data.__dict__, Organization, id)
        return True

    @strawberry.mutation
    async def add_project(self, data: ProjectCreateType) -> int:
        obj_id = await insert_obj(Project, data.__dict__)
        return obj_id

    @strawberry.mutation
    async def update_project(self, id: int, data: ProjectUpdateType) -> bool:
        await update_object(data.__dict__, Project, id)
        return True

    @strawberry.mutation
    async def add_task(self, data: TaskCreateType) -> int:
        task_data = {
            'name': data.name,
            'description': data.description,
            'is_done': data.is_done,
            'assigner_id': data.assigner_id,
            'color': data.color,
            'duration': data.duration,
            'difficulty': data.difficulty,
            'project_id': data.project_id,
            'group_id': data.group_id,
        }

        obj_id = await insert_task(Task, task_data, data.assignees if data.assignees else [])
        return obj_id

    @strawberry.mutation
    async def update_task(self, id: int, data: TaskUpdateType) -> bool:
        await update_object(data.__dict__, Task, id)
        # task = await Task.get(id=id)
        # group = await Group.get(id=task.group_id)

        # data_mailing = await prepare_data_mailing(task.assigner, task, group, redis)
        # if data_mailing:
        #     await send_task_updates(data_mailing)

        return True
