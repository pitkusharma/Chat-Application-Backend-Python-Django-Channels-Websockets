from django.urls import path
from .views.createConnection import CreateConnection
from .views.getPendingConnections import GetPendingConnections
from .views.performAction import PerformAction
from .views.getFormedConnections import GetFormedConnections


urlpatterns = [
    path('create', CreateConnection.as_view()),
    path('get/pending', GetPendingConnections.as_view()),
    path('get/formed', GetFormedConnections.as_view()),
    path('perform-action/<str:action>/<uuid:connection_id>', PerformAction.as_view()),
]

