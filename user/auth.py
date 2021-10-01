from fastapi_users.authentication import JWTAuthentication


SECRET = '134qwdefd219378cr2387crby623nxry324781ct6c3'


auth_backends = []

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

auth_backends.append(jwt_authentication)
