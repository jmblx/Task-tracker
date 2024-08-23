from collections.abc import Callable

from strawberry import Info

from auth.models import User
from gql.gql_types import GoogleRegDTO, UserType
from gql.graphql_utils import process_data_and_insert
from utils import get_func_data


def google_register(func: Callable) -> Callable:
    async def wrapper(self, info: Info, data: "GoogleRegDTO") -> "UserType":
        function_name, result_type = get_func_data(func)

        data_dict = data.__dict__
        data_dict["is_email_confirmed"] = data_dict.pop("emailVerified")
        data_dict["first_name"] = data_dict.pop("givenName")
        data_dict["last_name"] = (
            data_dict.pop("familyName")
            if data_dict.get("familyName") is not None
            else None
        )

        session = info.context["db"]

        obj, _, selected_fields = await process_data_and_insert(
            info, User, data_dict, session, function_name=function_name
        )

        # if not data_dict.get("is_email_confirmed"):
        #     await process_notifications(info, data_dict, obj)

        return result_type.from_instance(obj, selected_fields)

    return wrapper
