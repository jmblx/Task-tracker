import asyncio
import datetime

import asana
from asana.rest import ApiException
from pprint import pprint

from sqlalchemy import select, insert

from auth.models import User
from database import async_session_maker
from project.models import Project
from task.models import Task

from fastapi import APIRouter

router = APIRouter(prefix='/project')





def make_naive(dt):
    if dt is not None:
        return dt.replace(tzinfo=None)  # Преобразование aware datetime в naive datetime
    return None  # Возвращение None, если dt уже None



async def get_project_description(project_id):
    configuration = asana.Configuration()
    configuration.access_token = '2/1207064323890384/1207066247133573:bd4780cfc1b0c461d853e443d0fbe028'
    opts = {
        'opt_fields': 'notes'
    }
    api_client = asana.ApiClient(configuration)

    project_api_instance = asana.ProjectsApi(api_client)

    try:
        # Получение информации о проекте
        project = project_api_instance.get_project(project_id, opts)
        return project.get('notes', 'Описание не найдено')
    except ApiException as e:
        print(f"Ошибка при вызове ProjectsApi->get_project: {e}")
        return None



async def get_task_details(project_id, organization_id):
    configuration = asana.Configuration()
    configuration.access_token = '2/1207064323890384/1207066247133573:bd4780cfc1b0c461d853e443d0fbe028'
    api_client = asana.ApiClient(configuration)

    tasks_api_instance = asana.TasksApi(api_client)
    opt_fields = [
        'gid', 'name', 'due_on', 'permalink_url',
        'assignee.name', 'assignee.email', 'completed',
        'notes', 'custom_fields.display_value', 'custom_fields.name',
        'created_at', 'modified_at', 'completed_at', 'followers.name',
        'memberships.section.name', 'created_by.email', 'projects.name', 'notes'
    ]

    opts = {
        'limit': 50,
        'project': project_id,
        'opt_fields': ",".join(opt_fields)
    }

    tasks_summary = {
        'tasks': {},
        'project_description': await get_project_description(project_id),
        'project_name': None
    }

    try:
        api_response = tasks_api_instance.get_tasks(opts)
        tasks_data = list(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->get_tasks: %s\n" % e)
        return {}

    for task in tasks_data:
        print(task)
        for project in task.get('projects', []):
            tasks_summary["project_name"] = project['name']
        completed_at = task.get('completed_at')
        if completed_at:
            completed_at = datetime.datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
        current_date = datetime.date.today()
        if task.get('due_on'):
            due_on = datetime.datetime.strptime(task.get('due_on'), '%Y-%m-%d').date()
            duration = due_on - current_date
        else:
            duration = datetime.timedelta(seconds=0)
        task_details = {
            'assignee': task.get('assignee', {}),
            'completed_at': completed_at,
            'created_at': datetime.datetime.fromisoformat((task.get('created_at')).replace('Z', '+00:00')),
            'duration': duration,
            'permalink_url': task.get('permalink_url'),
            'name': task.get('name'),
            'notes': task.get('notes'),
            'custom_fields': {cf['name']: cf['display_value'] for cf in task.get('custom_fields', [])},
            'section': next((m['section']['name'] for m in task.get('memberships', []) if m.get('section')), None),
            'created_by': task.get('created_by', {}),
            'description': task.get('notes', 'Описание отсутствует'),
            "is_completed": task.get('completed', False),
        }
        tasks_summary['tasks'][task['gid']] = task_details
    async with async_session_maker() as session:
        project_result = await session.execute(
            insert(Project).values(
                name=tasks_summary["project_name"],
                description=tasks_summary["project_description"],
                organization_id=organization_id,
                asana_id=project_id
            ).returning(Project.id)
        )
        await session.flush()
        project_id = project_result.scalar()
        for gid, task_details in tasks_summary.get("tasks").items():
            print(task_details)
            added_at_naive = make_naive(task_details.get('created_at'))
            done_at_naive = make_naive(task_details.get('completed_at')) if task_details.get('completed_at') else None
            if gid == "project_description" or gid == "project_name":
                continue  # Пропускаем несоответствующие ключи

            author_email = task_details.get('created_by', {}).get('email')
            if author_email:
                author = (await session.execute(select(User).where(User.email == author_email))).scalar()

                diff = "easy" if task_details['custom_fields'].get("Приоритет", "") == "Низкий" else "hard"
                await session.commit()
                # Создание экземпляра задачи
                task = Task(
                    name=task_details['name'],
                    description=task_details['description'],
                    is_done=task_details['is_completed'],
                    added_at=added_at_naive,
                    done_at=done_at_naive,
                    assigner_id=author.id,
                    color="#FF1A1A",
                    difficulty=diff,
                    project_id=project_id,
                    duration=task_details['duration'],

                )
                session.add(task)
                await session.commit()
                print(author.id)

    return tasks_summary

@router.get('/setup/asana/{organization_id}/{project_id}')
async def setup_asana(organization_id: int, project_id: str):
    await get_task_details(project_id, organization_id)
    return {'status': 'ok'}
