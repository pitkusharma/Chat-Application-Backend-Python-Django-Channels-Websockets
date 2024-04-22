from channels.routing import URLRouter
from django.urls import path
from connections.routing import connection_routes

main_routing = URLRouter([
    path('connections/', connection_routes)
])