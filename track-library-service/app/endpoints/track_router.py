import uuid
from uuid import UUID

import keycloak
from keycloak import KeycloakOpenID
from typing import Optional, Callable

from app.auth.keycloak_auth import KeycloakAuthenticator
from app.creds import *

from functools import wraps
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.models.track import Track, CreateTrackRequest
from app.services.music_catalog_service import TrackCatalogService

track_catalog_router = APIRouter(prefix='/track-catalog', tags=['TrackCatalog'])

name = 'TrackCatalog with Recommendations Service'

keycloak_authenticator = KeycloakAuthenticator()

access_tokens = {}

keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=keycloak_client_id,
    client_secret_key=keycloak_client_secret,
    realm_name="mikhienkov",
    verify=False
)


def get_current_user(token: str):
    try:
        user_info = keycloak_openid.userinfo(token=token)
    except keycloak.exceptions.KeycloakAuthenticationError:
        raise HTTPException(status_code=403, detail={"details:": "Your access token is not valid"})

    return user_info


@track_catalog_router.get("/login")
def login(request: Request):
    response_content = keycloak_authenticator.login()
    return response_content


@track_catalog_router.get("/callback")
async def callback(request: Request):
    access_token = await keycloak_authenticator.callback(request)
    user_info = get_current_user(access_token)

    print("user_info: " + user_info.__str__())
    access_tokens.update({access_token: user_info})

    user = get_current_user(access_token)

    print("use: " + user.__str__())

    realm_access = user.get("realm_access", [])
    print(realm_access)
    roles = realm_access.get("roles", [])

    response_message = f"""
                                                                   <html>
                                                                       <head>
                                                                           <title>Your token</title>
                                                                           <style>
                                                                               body {{
                                                                                   font-size: 27px;
                                                                                   color: orange;
                                                                                   text-align: center;

                                                                               }}
                                                                               p {{
    word-break: break-all;
    white-space: normal;
}}
                                                                           </style>
                                                                       </head>
                                                                       <body>

                                                                           <p style="color: black;" >You're authorized now. Please use your token to get access to the services:</p>
                                                                            <p style="font-weight: bold;">{access_token}</p>
                                                                            <p style="color: black;">You may use service with next roles: {roles}</p>
                                                                              <a href="http://localhost:00/docs#">Go to DOCS</a>
                                                                       </body>
                                                                   </html>
                                                               """

    return HTMLResponse(response_message)


def keycloak_security(required_roles: Optional[list] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
                *args,
                **kwargs):

            token = kwargs.get("token")

            if token:
                user = get_current_user(token)

                realm_access = user.get("realm_access", [])
                roles = realm_access.get("roles", [])

                if not any(role in roles for role in required_roles):
                    error_message = f"""
                                                                                   <html>
                                                                                       <head>
                                                                                           <title>Insufficient permissions</title>
                                                                                           <style>
                                                                                               body {{
                                                                                                   font-size: 27px;
                                                                                                   color: black;
                                                                                                   text-align: center;
                                                                                               }}
                                                                                           </style>
                                                                                       </head>
                                                                                       <body>
                                                                                           <p>Permission for your role denied</p>
                                                                                           <p>You may use service only with next roles: {roles}</p>
                                                                                           <a href="http://localhost:80/track-api/track-catalog/login">Login</a>
                                                                                       </body>
                                                                                   </html>
                                                                               """
                    return HTMLResponse(content=error_message, status_code=403)

            else:
                error_message = f"""
                                                               <html>
                                                                   <head>
                                                                       <title>Unauthorized Access</title>
                                                                       <style>
                                                                           body {{
                                                                               font-size: 33px;
                                                                               color: red;
                                                                               text-align: center;
                                                                           }}
                                                                       </style>
                                                                   </head>
                                                                   <body>
                                                                       <p>You're not authorized. Please login with this URL first:</p>
                                                                       <a href="http://localhost:80/track-api/track-catalog/login">Login</a>
                                                                   </body>
                                                               </html>
                                                           """
                return HTMLResponse(content=error_message, status_code=403)

            return func(*args, **kwargs)

        return wrapper

    return decorator



@track_catalog_router.get('/')
@keycloak_security(["admin", "user"])
def get_tracks(track_catalog_service: TrackCatalogService = Depends(TrackCatalogService), token: str = None) -> list[
    Track]:
    return track_catalog_service.get_tracks()


# @track_catalog_router.get('/test')
# def get_tracks() -> str:
#     with tracer.start_as_current_span("server_request"):
#         return "it works!"



@track_catalog_router.get('/{track_id}')
@keycloak_security(["admin", "user"])
def get_track(track_id: UUID, track_catalog_service: TrackCatalogService = Depends(TrackCatalogService),
              token: str = None) -> Track:
    track = track_catalog_service.get_track_by_id(track_id)
    if track:
        return track.dict()
    else:
        raise HTTPException(404, f'Trackwith id={track_id} not found')



@track_catalog_router.post('/add')
@keycloak_security(["admin"])
def add_track(request: CreateTrackRequest,
              track_catalog_service: TrackCatalogService = Depends(TrackCatalogService), token: str = None) -> Track:
    new_track = track_catalog_service.add_track(
        name=request.name,
        author=request.author,
        genre=request.genre,
        description=request.description)
    return new_track.dict()



@track_catalog_router.put('/update/{track_id}')
@keycloak_security(["admin"])
def update_track(track_id: UUID, request: CreateTrackRequest,
                 track_catalog_service: TrackCatalogService = Depends(TrackCatalogService), token: str = None) -> Track:
    updated_track = track_catalog_service.update_track(track_id, request.name, request.author, request.genre,
                                                       request.description)
    return updated_track.dict()



@track_catalog_router.delete('/delete/{track_id}')
@keycloak_security(["admin"])
def delete_track(track_id: UUID, track_catalog_service: TrackCatalogService = Depends(TrackCatalogService),
                 token: str = None) -> None:
    track_catalog_service.delete_track(track_id)
    return {'message': 'Track deleted successfully'}
