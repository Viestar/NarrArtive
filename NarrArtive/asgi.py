"""
ASGI config for NarrArtive project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chats.routing import websocket_urlpatterns

""" 
This supports asynchronous features such as Websocket, Server-Sent-Events etc.
It is used especially for long-lived connections
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NarrArtive.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  #handles the HTTP request but in an asynchronous way
    "websocket": AuthMiddlewareStack(
        URLRouter( # deals with the WebSocket connection
            websocket_urlpatterns
        )
    ),
})
