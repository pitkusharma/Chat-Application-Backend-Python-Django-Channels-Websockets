import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from authentication.jwt_authentication import JWTAuthenticationMiddleware
from .routing import main_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChattingApplicationBackend.settings')

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthenticationMiddleware(
            main_routing
        ),
    }
)
