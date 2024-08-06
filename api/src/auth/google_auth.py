from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

from config import GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET


router = APIRouter(prefix='/auth/google')

# Объявляем необходимые переменные
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = 'http://localhost:8000/auth/google/callback'


def get_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": GOOGLE_OAUTH_CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )


@router.get('/')
def auth_google():
    flow = get_flow()
    authorization_url, _ = flow.authorization_url(prompt='consent')
    print(authorization_url)
    return RedirectResponse(authorization_url)


@router.get('/callback')
def auth_google_callback(request: Request):
    state = request.query_params.get('state')
    code = request.query_params.get('code')

    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    flow = get_flow()
    flow.fetch_token(code=code)

    credentials = flow.credentials
    print(credentials)
    session = flow.authorized_session()
    user_info = session.get('https://www.googleapis.com/oauth2/v2/userinfo').json()

    return user_info


def google_data_change(data: dict):
    data.update({"is_email_confirmed": True, "role_id": 1})
    return data
