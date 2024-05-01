"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from .channelsmiddilewayer import JwtAuthMiddleware
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from chat import routing
from posts import routing as  postrouting

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': JWTAuthMiddlewareStack(
            AllowedHostsOriginValidator(
                JwtAuthMiddleware(URLRouter(routing.websocket_urlpatterns+postrouting.websocket_urlpatterns))
            ),
        ),
    }
)




