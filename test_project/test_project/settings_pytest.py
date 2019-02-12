# Settings for testing with included docker-compose and pytest

from .settings import *  # noqa

# Subscribe from remote selenium container to docker-compose nginx container
NGINX_PUSH_STREAM_PUB_HOST = "localhost"
NGINX_PUSH_STREAM_PUB_PORT = "9080"

# Subscribe from local TravisCI machine to docker-compose nginx container
NGINX_PUSH_STREAM_SUB_HOST = "webserver"
NGINX_PUSH_STREAM_SUB_PORT = "80"
