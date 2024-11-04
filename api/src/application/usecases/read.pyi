class ReadUseCase:
    def __init__(
        self,
        _service: ServiceInterface,
        access_policy: AccessPolicyInterface,
        auth_service: AuthService,
    ):
        self._service = _service
        self.access_policy = access_policy
        self.auth_service = auth_service

    async def __call__(
        self,
        auth_token: str,
        search_data: dict[Any, Any],
        selected_fields: dict[Any, dict[Any, dict]],
        order_by: dict,
    ) -> list[]:
        required_data_requester, required_data_user, checks = await self.access_policy.get_required_data("read", selected_fields)
        logging.info([required_data_requester, required_data_user, checks])
        requester = await self.auth_service.get_user_by_token(auth_token, required_data_requester.get("user"))

        target_ = await self._service.get_many_by_fields(
            search_data, required_data_user
        )

        for target_ in target_:
            target__data = {"user": {"id": target_.id}}
            if not await self.access_policy.check_access(requester, required_data_requester, target__data, checks):
                logging.warning(f"Access denied for user {requester.id} to user {target_.id}")
                raise PermissionError(f"Access denied to user {target_.id}")

         = await self._service.get_many_by_fields(
            search_data, selected_fields, order_by
        )
        return