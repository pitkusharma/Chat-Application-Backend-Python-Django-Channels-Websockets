import jwt
import datetime
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.conf import settings
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


Users = get_user_model()

# Custom authentication class
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_token:
            return None
        jwt_token = jwt_token.replace('Bearer ', '')
        user, token_data = self.verify_token(jwt_token)
        return user, token_data

    @classmethod
    def verify_token(self, jwt_token):
        try:
            token_data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.JWT_ENCRYPTION_ALGORITHM,])
            expires_at = datetime.datetime.strptime(token_data['expires_at'], '%Y-%m-%d %H:%M:%S.%f')
        except:
            raise AuthenticationFailed("Invalid token")
        if expires_at < datetime.datetime.now():
            raise AuthenticationFailed("Expired token")
        try:
            user = Users.objects.get(id=token_data['user_id'])
        except:
            raise AuthenticationFailed('User does not exist')
        return user, token_data

    def authenticate_header(self, request):
        return 'Bearer'



# Websocket authentication middleware
class JWTAuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            token = list(
                filter(lambda x: x[0].decode().upper() == 'AUTHORIZATION', scope['headers'])
            )[0][1].decode()
            scope['user'], token_data = await database_sync_to_async(JWTAuthentication.verify_token)(token)
            scope['authenticated'] = True
        except Exception as e:
            scope['user'] = AnonymousUser()
            scope['authenticated'] = False
        finally:
            return await self.app(scope, receive, send)


class GenerateTokens:
    def __init__(self, user=None):
        self.user = user

    def generate_token(self, expiry_hours):
        data = {
            'user_id': str(self.user.id),
            'issued_at': str(datetime.datetime.now()),
            'expires_at': str(datetime.datetime.now() + datetime.timedelta(hours=expiry_hours))
        }
        token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ENCRYPTION_ALGORITHM)
        return token

    def access_token(self):
        return self.generate_token(settings.ACCESS_TOKEN_EXPIRY_HOURS)

    def refresh_token(self):
        return self.generate_token(settings.REFRESH_TOKEN_EXPIRY_HOURS)

