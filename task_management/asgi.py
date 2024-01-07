
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from chat.ChannelsJWTMiddleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django_asgi_app = get_asgi_application()
from chat.routing import ws_patterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # 'websocket' : URLRouter(ws_patterns),
    'websocket': JWTAuthMiddleware(
        URLRouter(
            ws_patterns
        )
    ),

    # WebSocket chat handler
    # "websocket": AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter(ws_patterns)
    #     )
    # ),
})