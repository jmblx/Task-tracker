import asana
from asana.rest import ApiException
from pprint import pprint

configuration = asana.Configuration()
configuration.access_token = '2/1207064323890384/1207066247133573:bd4780cfc1b0c461d853e443d0fbe028'
api_client = asana.ApiClient(configuration)

# create an instance of the API class
projects_api_instance = asana.ProjectsApi(api_client)
project_gid = "1207064217605219" # str | Globally unique identifier for the project.
opts = {
    'opt_fields': "created_at"
}

try:
    # Get a project
    api_response = projects_api_instance.get_project(project_gid, opts)
    print(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->get_project: %s\n" % e)