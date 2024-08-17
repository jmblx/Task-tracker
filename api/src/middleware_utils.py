from fastapi import Request


def form_state(
    request: Request, headers: dict[str, str], cookies: dict[str, str]
):
    """
    Формирует состояния запроса из заголовков и cookies
    """
    for header, attribute in headers.items():
        setattr(request.state, attribute, request.headers.get(header))

    for cookie, attribute in cookies.items():
        setattr(request.state, attribute, request.cookies.get(cookie))

    return request
