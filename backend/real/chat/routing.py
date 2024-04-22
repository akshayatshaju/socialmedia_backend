from django.urls import path
from . import consumers  
from channels.routing import ProtocolTypeRouter, URLRouter
websocket_urlpatterns = [
    path('ws/chat/<int:room_id>/',consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket':
        URLRouter(
            websocket_urlpatterns
        )
    ,
})