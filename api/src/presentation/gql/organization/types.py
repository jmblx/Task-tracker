from typing import Annotated, ForwardRef

import strawberry

from core.utils import GqlProtocol
from presentation.gql.graphql_utils import add_from_instance

ProjectType = ForwardRef("ProjectType")
UserType = ForwardRef("UserType")


@strawberry.type
@add_from_instance
class OrganizationType(GqlProtocol):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    staff: (
        list[
            Annotated[
                "UserType", strawberry.lazy("presentation.gql.user.types")
            ]
        ]
        | None
    ) = None
    projects: (
        list[
            Annotated[
                "ProjectType",
                strawberry.lazy("presentation.gql.project.types"),
            ]
        ]
        | None
    ) = None
    # workers: Optional[List[UserType]] = None
    # managers: Optional[List[UserType]] = None
