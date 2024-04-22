from django.urls import path
from .consumer import ConnectionHandleConsumer
from channels.routing import URLRouter


connection_routes = URLRouter([
    path('main/', ConnectionHandleConsumer.as_asgi())
])