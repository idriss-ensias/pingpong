from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/yggip/(?P<game>\w+)/$', consumers.PlayerConsumer.as_asgi()),
    re_path(r'ws/skirt/(?P<game>\w+)/$', consumers.TheConsumer.as_asgi()),
    re_path(r'ws/yggip/nino/(?P<nino>\w+)/$', consumers.NinoConsumer.as_asgi()),
    re_path(r'ws/yggip/pong/(?P<player>\w+)/(?P<mode>\w+)/$', consumers.PageConsumer.as_asgi()),
]